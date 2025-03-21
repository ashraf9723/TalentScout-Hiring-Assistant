"""
This module manages the chat flow, context, and state of the conversation.
"""
import google.generativeai as genai
import os
from prompt_engine import PromptEngine

class ChatManager:
    def __init__(self, api_key=None):
        """Initialize the chat manager with the API key and conversation state."""
        # Set Google API key
        if api_key:
            genai.configure(api_key=api_key)
        elif os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        else:
            raise ValueError("Google API key must be provided or set as an environment variable.")

        # Initialize the Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-pro')

        # Initialize the prompt engine
        self.prompt_engine = PromptEngine()

        # Initialize conversation state
        self.conversation_stage = "greeting"  # Stages: greeting, info_gathering, tech_questions, end
        self.candidate_info = {
            "full_name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "desired_position": None,
            "location": None,
            "tech_stack": None
        }

        # Initialize conversation history
        self.chat = self.model.start_chat(history=[])
        # Add system message to conversation
        self._add_system_message(self.prompt_engine.get_system_message())

    def process_message(self, user_message):
        """
        Process a user message, update the conversation state, and generate a response.

        Args:
            user_message (str): The message from the user

        Returns:
            str: The assistant's response
        """
        # Check for exit commands
        if user_message.lower() in ["exit", "quit", "bye"]:
            self.conversation_stage = "end"
            return self._generate_response(self.prompt_engine.get_end_conversation_prompt())

        # Process based on current conversation stage
        if self.conversation_stage == "greeting":
            response = self._handle_greeting()
        elif self.conversation_stage == "info_gathering":
            # Extract info from the user message before responding
            self._extract_candidate_info(user_message)
            response = self._handle_info_gathering()
        elif self.conversation_stage == "tech_questions":
            response = self._handle_tech_questions()
        elif self.conversation_stage == "end":
            response = self._generate_response(self.prompt_engine.get_end_conversation_prompt())
        else:
            response = "I'm sorry, something went wrong. Let's start over."
            self.conversation_stage = "greeting"

        return response

    def _handle_greeting(self):
        """Handle the greeting stage and transition to info gathering."""
        self.conversation_stage = "info_gathering"
        return self._generate_response(self.prompt_engine.get_greeting_prompt())

    def _handle_info_gathering(self):
        """
        Handle the information gathering stage.
        Check if all required information has been collected.
        """
        # Check if all required information has been collected
        missing_info = self._get_missing_info()

        if not missing_info:
            # All info collected, move to technical questions
            self.conversation_stage = "tech_questions"
            return self._handle_tech_questions()
        else:
            # Continue gathering missing information
            prompt = self.prompt_engine.get_info_gathering_prompt(missing_info)
            return self._generate_response(prompt)

    def _handle_tech_questions(self):
        """Handle the technical questions stage."""
        # Move to end stage after generating questions
        self.conversation_stage = "end"

        # Generate questions based on tech stack
        tech_stack = self.candidate_info["tech_stack"]
        prompt = self.prompt_engine.get_tech_questions_prompt(tech_stack)
        return self._generate_response(prompt)

    def _extract_candidate_info(self, message):
        """
        Extract candidate information from the message and update the state.
        """
        # Create a system prompt for information extraction
        system_prompt = """
        Extract the following information from the conversation if available:
        - Full Name
        - Email Address
        - Phone Number
        - Years of Experience
        - Desired Position(s)
        - Current Location
        - Tech Stack (languages, frameworks, databases, tools)
        
        Format the response as JSON with the fields:
        full_name, email, phone, experience, desired_position, location, tech_stack
        
        If a piece of information is not provided, keep the value as null.
        If information was previously provided, include it in the response.
        """

        try:
            # Create a temporary chat for extraction without affecting main conversation
            extraction_model = genai.GenerativeModel('gemini-1.5-pro')
            extraction_chat = extraction_model.start_chat()

            # Get the current conversation content as context
            conversation_content = ""
            for message in self.chat.history:
                role = "User" if message.role == "user" else "Assistant"
                conversation_content += f"{role}: {message.parts[0].text}\n"

            # Add the current message
            conversation_content += f"User: {message}\n"

            # Send to extraction chat
            extraction_chat.send_message(f"{system_prompt}\n\nHere is the conversation:\n{conversation_content}")

            extracted_info = extraction_chat.last.text

            # Basic error handling for JSON parsing
            try:
                import json
                # Find JSON in the response (it might have explanatory text around it)
                import re
                json_match = re.search(r'(\{.*\})', extracted_info, re.DOTALL)
                if json_match:
                    extracted_json = json_match.group(1)
                    info_dict = json.loads(extracted_json)

                    # Update candidate info with extracted information (only if not None)
                    for key, value in info_dict.items():
                        if value is not None and value != "":
                            self.candidate_info[key] = value

            except json.JSONDecodeError:
                print("Failed to parse JSON from extraction")

        except Exception as e:
            print(f"Error extracting information: {e}")

    def _get_missing_info(self):
        """Return a list of missing candidate information fields."""
        missing = []
        for key, value in self.candidate_info.items():
            if value is None:
                # Convert keys from snake_case to readable format
                readable_key = key.replace("_", " ").title()
                missing.append(readable_key)

        return missing

    def _add_system_message(self, message):
        """Add a system message to the chat history."""
        # For Gemini, we'll prepend "System:" to simulate system messages
        self.chat.send_message(f"System: {message}")

    def _generate_response(self, prompt):
        """
        Generate a response using the Gemini API.

        Args:
            prompt (str): The prompt to guide the response generation

        Returns:
            str: The generated response
        """
        try:
            # Add the guidance prompt as a system message
            guidance_message = f"System: {prompt}"

            # Send the system guidance without adding to visible history
            temp_response = self.model.generate_content(guidance_message)

            # Now send the user's last message (which is already in history)
            # or a generic prompt if we're just starting
            if not self.chat.history or self.chat.history[-1].role != "user":
                response = self.chat.send_message("Hello")
            else:
                # The user's message is already in the chat history, so we just generate the next response
                # This is just to get the assistant's response given the system guidance
                response = self.model.generate_content("Based on the previous conversation, provide the next assistant response.")

            return response.text

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your request. Could you please try again?"
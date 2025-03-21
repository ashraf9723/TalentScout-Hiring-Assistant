"""
This module handles prompt templates and generation logic for the TalentScout hiring assistant.
"""


class PromptEngine:
    def __init__(self):
        """Initialize the prompt engine with templates for different conversation stages."""
        # System message that defines the chatbot's role and capabilities
        self.system_message = """
        You are an AI-powered hiring assistant for TalentScout, a recruitment agency specializing in technology placements.
        Your name is TalentScout Assistant. Your job is to conduct initial candidate screening by gathering
        essential information and asking relevant technical questions based on the candidate's declared tech stack.

        Follow these guidelines:
        1. Be professional, friendly, and concise.
        2. Collect all required information before proceeding to technical questions.
        3. Generate 3-5 relevant technical questions based on the candidate's tech stack.
        4. Maintain the conversation context.
        5. If the candidate types 'exit', 'quit', or 'bye', end the conversation politely.
        6. Don't ask for information that has already been provided.
        7. If a candidate doesn't provide the requested information, politely ask again.

        Required information to collect:
        - Full Name
        - Email Address
        - Phone Number
        - Years of Experience
        - Desired Position(s)
        - Current Location
        - Tech Stack (languages, frameworks, databases, tools)
        """

        # Template for the initial greeting
        self.greeting_template = """
        Greet the candidate professionally and introduce yourself as TalentScout Assistant.
        Explain that you'll be collecting some basic information and asking technical questions
        based on their tech stack to help with the initial screening process.
        Let them know they can type 'exit', 'quit', or 'bye' at any time to end the conversation.
        """

        # Template for gathering candidate information
        self.info_gathering_template = """
        Based on our conversation so far, I need to collect the following information from the candidate:

        {missing_info}

        Ask for the next piece of missing information in a conversational way. If multiple pieces are missing,
        ask for them one at a time, starting with the most basic (name, then contact info, etc.).

        Be polite and professional. Don't phrase it as a form or checklist.
        """

        # Template for generating technical questions
        self.tech_questions_template = """
        The candidate has shared their tech stack: {tech_stack}

        Generate 3-5 relevant technical questions to assess their proficiency in each technology they've mentioned.
        The questions should:
        1. Be specific to the technologies mentioned
        2. Range from basic to intermediate difficulty
        3. Allow the candidate to demonstrate both theoretical knowledge and practical experience
        4. Not be simple yes/no questions, but require explanatory answers

        Present the questions in a conversational manner, not as a numbered list.
        """

        # Template for ending the conversation
        self.end_conversation_template = """
        The conversation needs to end now. Thank the candidate for their time and information.
        Let them know that TalentScout will review their information and get back to them
        regarding the next steps in the hiring process. Wish them good luck and say goodbye professionally.
        """

        # Template for fallback responses
        self.fallback_template = """
        The candidate's input is unclear or doesn't directly answer the question asked.
        Respond politely and redirect to the current information-gathering objective.
        Remind them what information you're currently asking for, but don't be pushy.
        """

    def get_system_message(self):
        """Return the system message that defines the assistant's role."""
        return self.system_message

    def get_greeting_prompt(self):
        """Return the greeting prompt."""
        return self.greeting_template

    def get_info_gathering_prompt(self, missing_info):
        """Return a prompt to gather missing candidate information."""
        return self.info_gathering_template.format(missing_info=missing_info)

    def get_tech_questions_prompt(self, tech_stack):
        """Return a prompt to generate technical questions based on tech stack."""
        return self.tech_questions_template.format(tech_stack=tech_stack)

    def get_end_conversation_prompt(self):
        """Return a prompt to end the conversation professionally."""
        return self.end_conversation_template

    def get_fallback_prompt(self):
        """Return a prompt for handling unclear or unexpected inputs."""
        return self.fallback_template
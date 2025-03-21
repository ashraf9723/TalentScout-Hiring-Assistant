# TalentScout Hiring Assistant

## Project Overview
TalentScout Hiring Assistant is an intelligent chatbot designed to assist recruitment agencies in the initial screening of technical candidates. The assistant engages with candidates in a conversational manner, collecting essential information such as contact details, experience, desired positions, and tech stack. Based on the candidate's declared technologies, the assistant generates relevant technical questions to assess their proficiency.

## Features
- **Professional greeting and introduction** with clear purpose explanation
- **Information gathering** for essential candidate details
- **Tech stack assessment** with tailored technical questions
- **Context-aware conversations** that maintain flow and coherence
- **Graceful conversation ending** with clear next steps
- **Intuitive Streamlit UI** for seamless interaction

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Google API key for Gemini

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running the Application
1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the address shown in the terminal (typically http://localhost:8501)

## Usage Guide
1. The chatbot will greet you upon initialization
2. Respond to the chatbot's questions about your information and experience
3. When asked about your tech stack, list all relevant technologies you're proficient in
4. The chatbot will generate technical questions based on your declared tech stack
5. After the technical questions, the conversation will conclude with next steps
6. Type 'exit', 'quit', or 'bye' at any time to end the conversation immediately

## Technical Details

### Libraries Used
- **Streamlit**: For the user interface
- **Google Generative AI**: For accessing Gemini models
- **python-dotenv**: For environment variable management

### Architecture
The application follows a modular design with clear separation of concerns:

1. **app.py**: Main Streamlit application that handles the UI and user interaction
2. **chat_manager.py**: Manages the conversation flow, state, and context
3. **prompt_engine.py**: Contains prompt templates for different conversation stages
4. **utils.py**: Utility functions for input validation and formatting

### Prompt Design
The prompts are carefully crafted to:
1. **Define clear roles and objectives** through the system message
2. **Guide the conversation flow** through stage-specific templates
3. **Maintain context** by including relevant conversation history
4. **Extract information efficiently** using structured extraction prompts
5. **Generate relevant technical questions** based on specific tech stacks

The prompt design ensures the chatbot remains focused on its purpose while providing a natural conversational experience.

## Challenges & Solutions

### Challenge 1: Information Extraction
**Problem**: Reliably extracting structured information from unstructured conversation.
**Solution**: Using the language model itself for information extraction by prompting it to parse the conversation and return structured data.

### Challenge 2: Context Management
**Problem**: Maintaining conversation context across multiple turns.
**Solution**: Implementing a stateful conversation manager that tracks the conversation stage and accumulated information.

### Challenge 3: Technical Question Generation
**Problem**: Generating relevant technical questions for diverse tech stacks.
**Solution**: Creating a dynamic prompt that incorporates the candidate's specific technologies and guides the model to generate appropriately challenging questions.

### Challenge 4: User Experience
**Problem**: Creating a natural conversational flow while still gathering structured information.
**Solution**: Designing prompts that encourage conversational responses while maintaining a clear information-gathering objective.

## Future Enhancements
- **Multilingual support** for international candidates
- **Sentiment analysis** to gauge candidate engagement
- **Response scoring** to evaluate technical answer quality
- **Integration with ATS** (Applicant Tracking Systems)
- **Custom question templates** for specific roles

## License
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
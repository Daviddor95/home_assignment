# HMO Information Chatbot

A bilingual (English/Hebrew) chatbot system for HMO (Health Maintenance Organization) services that collects user information and answers questions based on their insurance plan and knowledge base.

## Project Structure

```
project/
├── backend/
│   ├── knowledge_base/
│   │   ├── alternative_services.html
│   │   ├── communication_clinic_services.html
│   │   ├── dental_services.html
│   │   ├── optometry_services.html
│   │   ├── pregnancy_services.html
│   │   └── workshops_services.html
│   ├── .env
│   ├── app.py
│   ├── logging_config.py
│   ├── prompts.py
│   └── requirements.txt
└── frontend/
    ├── requirements.txt
    └── streamlit_app.py
```

## Features

- **Bilingual Support**: Full English and Hebrew language support with RTL text rendering
- **Information Collection**: Natural conversation flow to collect user details (name, ID, HMO, etc.)
- **Data Validation**: Strict validation for Israeli ID numbers and HMO card numbers
- **Knowledge Base Integration**: Answers questions based on HTML knowledge base files
- **Modern UI**: Clean Streamlit interface with responsive design
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Daviddor95/home_assignment.git
cd home_assignment
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend` directory with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
```

**Important**: Replace the placeholder values with your actual Azure OpenAI endpoint and API key.

### 4. Knowledge Base Setup

Ensure all HTML files are present in the `backend/knowledge_base/` directory:
- `alternative_services.html`
- `communication_clinic_services.html`
- `dental_services.html`
- `optometry_services.html`
- `pregnancy_services.html`
- `workshops_services.html`

These files should contain the HMO service information in HTML format.

### 5. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install frontend dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### 1. Start the Backend Server

In the backend directory with your virtual environment activated:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The FastAPI backend will be available at: http://localhost:8000

You can view the API documentation at: http://localhost:8000/docs

### 2. Start the Frontend Application

In a separate terminal, navigate to the frontend directory with your virtual environment activated:

```bash
streamlit run streamlit_app.py
```

The Streamlit frontend will be available at: http://localhost:8501

## API Endpoints

### POST `/chat`

Handles the information collection phase of the conversation.

**Request Body**:
```json
{
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! I'd like to collect some information..."}
  ],
  "user_info": null,
  "language": "en"
}
```

**Response**:
```json
{
  "phase": "collecting|confirming",
  "assistant": "Assistant response text",
  "user_info": {...} // Only present when phase is "confirming"
}
```

### POST `/ask`

Handles question-answering based on the knowledge base.

**Request Body**:
```json
{
  "user_info": {
    "first_name": "John",
    "last_name": "Doe",
    "id_number": "123456789",
    "gender": "male",
    "age": 30,
    "hmo": "מכבי",
    "card_number": "987654321",
    "tier": "זהב"
  },
  "history": [...],
  "new_message": "What services are available?",
  "language": "en"
}
```

**Response**:
```json
{
  "assistant": "Based on your Gold tier plan with Maccabi..."
}
```

## User Information Requirements

The system collects and validates the following user information:

- **First Name**: User's first name
- **Last Name**: User's last name  
- **ID Number**: 9-digit Israeli ID number
- **Gender**: male, female, or other
- **Age**: Between 0 and 120
- **HMO**: One of מכבי, מאוחדת, כללית
- **Card Number**: 9-digit HMO card number
- **Tier**: Insurance tier (זהב, כסף, ארד)

## Language Support

The application supports:
- **English**: Left-to-right text rendering
- **Hebrew**: Right-to-left text rendering with proper RTL CSS styling

Switch languages using the sidebar in the Streamlit interface.

## Configuration

### Backend Configuration
- **Logging**: Configured to log to both file (`chatbot.log`) and console
- **CORS**: Currently disabled but can be enabled for cross-origin requests
- **Model**: Uses GPT-4o by default (configurable in `get_llm_response()`)

### Frontend Configuration
- **API URL**: Set to `http://localhost:8000` (modify in `streamlit_app.py` if needed)
- **Page Config**: Centered layout with health icon
- **Session State**: Maintains conversation history and user state

## Log Files

The backend creates a `chatbot.log` file in the backend directory containing:
- Information extraction attempts
- Successful user validations
- API call errors
- Knowledge base loading status

## Troubleshooting

### Common Issues

1. **"Azure OpenAI client is not configured"**
   - Check your `.env` file exists and contains valid credentials
   - Ensure environment variables are properly loaded

2. **"Knowledge base files not found"**
   - Verify all HTML files exist in `backend/knowledge_base/`
   - Check file permissions and encoding (should be UTF-8)

3. **"Could not connect to the backend"**
   - Ensure the FastAPI server is running on port 8000
   - Check if another application is using port 8000

4. **Hebrew text not displaying correctly**
   - The RTL styling should automatically apply when Hebrew is selected
   - Ensure your browser supports RTL text rendering

### Debug Mode

To enable more detailed logging, modify the logging level in `logging_config.py`:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Development Notes

- The system uses Pydantic for data validation
- All user information is validated according to Israeli standards
- Knowledge base content is loaded from all HTML files and combined
- The conversation flow is managed through session state
- Error handling includes graceful fallbacks for API failures

## Support

For technical support or questions:
- Check the FastAPI docs at http://localhost:8000/docs when running
- Review the `chatbot.log` file for error details
- Ensure all dependencies are properly installed
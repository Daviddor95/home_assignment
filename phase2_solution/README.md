\# HMO Information Chatbot



A bilingual (English/Hebrew) chatbot system for HMO (Health Maintenance Organization) services that collects user information and answers questions based on their insurance plan and knowledge base.



\## Project Structure



```

project/

├── backend/

│   ├── knowledge\_base/

│   │   ├── alternative\_services.html

│   │   ├── communication\_clinic\_services.html

│   │   ├── dental\_services.html

│   │   ├── optometry\_services.html

│   │   ├── pregnancy\_services.html

│   │   └── workshops\_services.html

│   ├── .env

│   ├── app.py

│   ├── logging\_config.py

│   ├── prompts.py

│   └── requirements.txt

└── frontend/

&nbsp;   ├── requirements.txt

&nbsp;   └── streamlit\_app.py

```



\## Features



\- \*\*Bilingual Support\*\*: Full English and Hebrew language support with RTL text rendering

\- \*\*Information Collection\*\*: Natural conversation flow to collect user details (name, ID, HMO, etc.)

\- \*\*Data Validation\*\*: Strict validation for Israeli ID numbers and HMO card numbers

\- \*\*Knowledge Base Integration\*\*: Answers questions based on HTML knowledge base files

\- \*\*Modern UI\*\*: Clean Streamlit interface with responsive design

\- \*\*Comprehensive Logging\*\*: Detailed logging for debugging and monitoring



\## Prerequisites



\- Python 3.8 or higher

\- Azure OpenAI API access

\- Git (for cloning the repository)



\## Installation



\### 1. Clone the Repository



```bash

git clone https://github.com/Daviddor95/home\_assignment.git

cd home\_assignment

```



\### 2. Backend Setup



Navigate to the backend directory:



```bash

cd backend

```



Create and activate a virtual environment:



```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# macOS/Linux

python3 -m venv venv

source venv/bin/activate

```



Install backend dependencies:



```bash

pip install -r requirements.txt

```



\### 3. Environment Configuration



Create a `.env` file in the `backend` directory with your Azure OpenAI credentials:



```env

AZURE\_OPENAI\_ENDPOINT=https://your-resource-name.openai.azure.com/

AZURE\_OPENAI\_API\_KEY=your-api-key-here

```



\*\*Important\*\*: Replace the placeholder values with your actual Azure OpenAI endpoint and API key.



\### 4. Knowledge Base Setup



Ensure all HTML files are present in the `backend/knowledge\_base/` directory:

\- `alternative\_services.html`

\- `communication\_clinic\_services.html`

\- `dental\_services.html`

\- `optometry\_services.html`

\- `pregnancy\_services.html`

\- `workshops\_services.html`



These files should contain the HMO service information in HTML format.



\### 5. Frontend Setup



Open a new terminal and navigate to the frontend directory:



```bash

cd frontend

```



Create and activate a virtual environment:



```bash

\# Windows

python -m venv venv

venv\\Scripts\\activate



\# macOS/Linux

python3 -m venv venv

source venv/bin/activate

```



Install frontend dependencies:



```bash

pip install -r requirements.txt

```



\## Running the Application



\### 1. Start the Backend Server



In the backend directory with your virtual environment activated:



```bash

uvicorn app:app --host 0.0.0.0 --port 8000 --reload

```



The FastAPI backend will be available at: http://localhost:8000



You can view the API documentation at: http://localhost:8000/docs



\### 2. Start the Frontend Application



In a separate terminal, navigate to the frontend directory with your virtual environment activated:



```bash

streamlit run streamlit\_app.py

```



The Streamlit frontend will be available at: http://localhost:8501



\## API Endpoints



\### POST `/chat`

Handles the information collection phase of the conversation.



\*\*Request Body\*\*:

```json

{

&nbsp; "history": \[

&nbsp;   {"role": "user", "content": "Hello"},

&nbsp;   {"role": "assistant", "content": "Hi! I'd like to collect some information..."}

&nbsp; ],

&nbsp; "user\_info": null,

&nbsp; "language": "en"

}

```



\*\*Response\*\*:

```json

{

&nbsp; "phase": "collecting|confirming",

&nbsp; "assistant": "Assistant response text",

&nbsp; "user\_info": {...} // Only present when phase is "confirming"

}

```



\### POST `/ask`

Handles question-answering based on the knowledge base.



\*\*Request Body\*\*:

```json

{

&nbsp; "user\_info": {

&nbsp;   "first\_name": "John",

&nbsp;   "last\_name": "Doe",

&nbsp;   "id\_number": "123456789",

&nbsp;   "gender": "male",

&nbsp;   "age": 30,

&nbsp;   "hmo": "מכבי",

&nbsp;   "card\_number": "987654321",

&nbsp;   "tier": "זהב"

&nbsp; },

&nbsp; "history": \[...],

&nbsp; "new\_message": "What services are available?",

&nbsp; "language": "en"

}

```



\*\*Response\*\*:

```json

{

&nbsp; "assistant": "Based on your Gold tier plan with Maccabi..."

}

```



\## User Information Requirements



The system collects and validates the following user information:



\- \*\*First Name\*\*: User's first name

\- \*\*Last Name\*\*: User's last name  

\- \*\*ID Number\*\*: 9-digit Israeli ID number

\- \*\*Gender\*\*: male, female, or other

\- \*\*Age\*\*: Between 0 and 120

\- \*\*HMO\*\*: One of מכבי, מאוחדת, כללית

\- \*\*Card Number\*\*: 9-digit HMO card number

\- \*\*Tier\*\*: Insurance tier (זהב, כסף, ארד)



\## Language Support



The application supports:

\- \*\*English\*\*: Left-to-right text rendering

\- \*\*Hebrew\*\*: Right-to-left text rendering with proper RTL CSS styling



Switch languages using the sidebar in the Streamlit interface.



\## Configuration



\### Backend Configuration

\- \*\*Logging\*\*: Configured to log to both file (`chatbot.log`) and console

\- \*\*CORS\*\*: Currently disabled but can be enabled for cross-origin requests

\- \*\*Model\*\*: Uses GPT-4o by default (configurable in `get\_llm\_response()`)



\### Frontend Configuration

\- \*\*API URL\*\*: Set to `http://localhost:8000` (modify in `streamlit\_app.py` if needed)

\- \*\*Page Config\*\*: Centered layout with health icon

\- \*\*Session State\*\*: Maintains conversation history and user state



\## Log Files



The backend creates a `chatbot.log` file in the backend directory containing:

\- Information extraction attempts

\- Successful user validations

\- API call errors

\- Knowledge base loading status



\## Troubleshooting



\### Common Issues



1\. \*\*"Azure OpenAI client is not configured"\*\*

&nbsp;  - Check your `.env` file exists and contains valid credentials

&nbsp;  - Ensure environment variables are properly loaded



2\. \*\*"Knowledge base files not found"\*\*

&nbsp;  - Verify all HTML files exist in `backend/knowledge\_base/`

&nbsp;  - Check file permissions and encoding (should be UTF-8)



3\. \*\*"Could not connect to the backend"\*\*

&nbsp;  - Ensure the FastAPI server is running on port 8000

&nbsp;  - Check if another application is using port 8000



4\. \*\*Hebrew text not displaying correctly\*\*

&nbsp;  - The RTL styling should automatically apply when Hebrew is selected

&nbsp;  - Ensure your browser supports RTL text rendering



\### Debug Mode



To enable more detailed logging, modify the logging level in `logging\_config.py`:



```python

logging.basicConfig(level=logging.DEBUG, ...)

```



\## Development Notes



\- The system uses Pydantic for data validation

\- All user information is validated according to Israeli standards

\- Knowledge base content is loaded from all HTML files and combined

\- The conversation flow is managed through session state

\- Error handling includes graceful fallbacks for API failures



\## Support



For technical support or questions:

\- Check the FastAPI docs at http://localhost:8000/docs when running

\- Review the `chatbot.log` file for error details

\- Ensure all dependencies are properly installed


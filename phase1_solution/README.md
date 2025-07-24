\# National Insurance Form Extractor



A Streamlit‑based web app that uses Azure Document Intelligence (Form Recognizer) and Azure OpenAI to \*\*OCR\*\* National Insurance forms (Hebrew or English) and extract a structured JSON payload of all key fields.



---



\## Table of Contents



1\. \[Features](#features)  

2\. \[Prerequisites](#prerequisites)  

3\. \[Installation](#installation)  

4\. \[Configuration](#configuration)  

5\. \[Running the App](#running-the-app)  

6\. \[Project Structure](#project-structure)  

7\. \[Usage](#usage)  



---



\## Features



\- Upload PDF or image (JPG/PNG) files of the National Insurance Institute form.  

\- Automatic OCR via Azure Form Recognizer.  

\- Language detection (Hebrew vs. English).  

\- Field extraction to JSON using Azure OpenAI (GPT‑4o).  

\- Validation and reporting of any missing or empty fields.  



---



\## Prerequisites



\- Python 3.8 or higher  

\- An Azure subscription with:

&nbsp; - \*\*Form Recognizer\*\* resource  

&nbsp; - \*\*OpenAI\*\* resource (preview API enabled)  

\- A terminal/shell for running commands  

\- Git (optional, for cloning the repo)



---



\## Installation



1\. \*\*Clone the repository\*\*  

&nbsp;  ```bash

&nbsp;  git clone https://github.com/Daviddor95/home\_assignment.git

&nbsp;  cd home\_assignment



2\. \*\*Create and activate a virtual environment\*\*



&nbsp;  ```bash

&nbsp;  python3 -m venv venv

&nbsp;  source venv/bin/activate   # macOS/Linux

&nbsp;  venv\\Scripts\\activate      # Windows

&nbsp;  ```



3\. \*\*Install dependencies\*\*



&nbsp;  ```bash

&nbsp;  pip install --upgrade pip

&nbsp;  pip install -r requirements.txt

&nbsp;  ```



&nbsp;  The `requirements.txt` includes:



&nbsp;  \* streamlit>=1.32.0

&nbsp;  \* python-dotenv>=1.0.1

&nbsp;  \* azure‑ai‑formrecognizer>=3.3.2

&nbsp;  \* azure‑core>=1.30.1

&nbsp;  \* openai>=1.30.1\&#x20;



---



\## Configuration



1\. \*\*Create a `.env` file\*\* in the project root with the following entries:



&nbsp;  ```dotenv

&nbsp;  AZURE\_FORM\_RECOGNIZER\_ENDPOINT=<your-form-recognizer-endpoint>

&nbsp;  AZURE\_FORM\_RECOGNIZER\_KEY=<your-form-recognizer-key>

&nbsp;  AZURE\_OPENAI\_ENDPOINT=<your-openai-endpoint>

&nbsp;  AZURE\_OPENAI\_API\_KEY=<your-openai-api-key>

&nbsp;  ```



2\. \*\*Ensure\*\* these environment variables are valid. The app will terminate on startup if any are missing .



---



\## Running the App



To launch the Streamlit interface:



```bash

streamlit run form\_extractor\_app.py

```



\* Open your browser at the local URL printed in the console (usually `http://localhost:8501`).

\* Use the file uploader to select a PDF or image.

\* View the extracted OCR text, detected language, JSON output, and any warnings for missing fields.



---



\## Project Structure



```

home\_assignment/

├── .env                     # Environment variables (not committed)

├── form\_extractor\_app.py    # Main Streamlit app :contentReference\[oaicite:2]{index=2}

├── requirements.txt         # Python dependencies :contentReference\[oaicite:3]{index=3}

└── README.md                # This installation \& usage guide

```



---



\## Usage



1\. \*\*Upload\*\* a form (PDF/JPG/PNG).

2\. \*\*Wait\*\* for OCR processing and JSON extraction.

3\. \*\*Review\*\* the JSON and any validation warnings.

4\. \*\*Export\*\* or copy the JSON as needed for downstream workflows.




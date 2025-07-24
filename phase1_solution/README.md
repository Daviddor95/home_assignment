# National Insurance Form Extractor

A Streamlit-based web app that uses Azure Document Intelligence (Form Recognizer) and Azure OpenAI to **OCR** National Insurance forms (Hebrew or English) and extract a structured JSON payload of all key fields.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Running the App](#running-the-app)  
6. [Project Structure](#project-structure)  
7. [Usage](#usage)  

---

## Features

- Upload PDF or image (JPG/PNG) files of the National Insurance Institute form.  
- Automatic OCR via Azure Form Recognizer.  
- Language detection (Hebrew vs. English).  
- Field extraction to JSON using Azure OpenAI (GPT-4o).  
- Validation and reporting of any missing or empty fields.  

---

## Prerequisites

- Python 3.8 or higher  
- An Azure subscription with:
  - **Form Recognizer** resource  
  - **OpenAI** resource (preview API enabled)  
- A terminal/shell for running commands  
- Git (optional, for cloning the repo)

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/Daviddor95/home_assignment.git
   cd home_assignment
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   The `requirements.txt` includes:

   * streamlit>=1.32.0
   * python-dotenv>=1.0.1
   * azure-ai-formrecognizer>=3.3.2
   * azure-core>=1.30.1
   * openai>=1.30.1 

---

## Configuration

1. **Create a `.env` file** in the project root with the following entries:

   ```dotenv
   AZURE_FORM_RECOGNIZER_ENDPOINT=<your-form-recognizer-endpoint>
   AZURE_FORM_RECOGNIZER_KEY=<your-form-recognizer-key>
   AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
   AZURE_OPENAI_API_KEY=<your-openai-api-key>
   ```

2. **Ensure** these environment variables are valid. The app will terminate on startup if any are missing.

---

## Running the App

To launch the Streamlit interface:

```bash
streamlit run form_extractor_app.py
```

* Open your browser at the local URL printed in the console (usually `http://localhost:8501`).
* Use the file uploader to select a PDF or image.
* View the extracted OCR text, detected language, JSON output, and any warnings for missing fields.

---

## Project Structure

```
home_assignment/
├── .env                     # Environment variables (not committed)
├── form_extractor_app.py    # Main Streamlit app
├── requirements.txt         # Python dependencies
└── README.md                # This installation & usage guide
```

---

## Usage

1. **Upload** a form (PDF/JPG/PNG).
2. **Wait** for OCR processing and JSON extraction.
3. **Review** the JSON and any validation warnings.
4. **Export** or copy the JSON as needed for downstream workflows.
import os
import json
import logging
from datetime import datetime
import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
from typing import Tuple, Dict, List, Any


load_dotenv()

# Configure structured logging
timestamp = datetime.utcnow().isoformat()
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("form_extractor")

# Configuration - set these environment variables
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Validate configuration at startup
for var in ["AZURE_FORM_RECOGNIZER_ENDPOINT", "AZURE_FORM_RECOGNIZER_KEY",
            "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"]:
    if not globals().get(var):
        logger.error(f"Environment variable {var} is not set.")
        raise SystemExit(f"Missing config: {var}")

# Initialize clients
def init_clients() -> Tuple[DocumentAnalysisClient, AzureOpenAI]:
    logger.info("Initializing Azure clients...")
    form_recognizer_client = DocumentAnalysisClient(
        endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY)
    )
    openai_client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-07-01-preview",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )
    return form_recognizer_client, openai_client

# OCR via Azure Document Intelligence
def analyze_document(client: DocumentAnalysisClient, file_bytes: bytes) -> str:
    logger.info("Submitting document for OCR...")
    poller = client.begin_analyze_document("prebuilt-layout", document=file_bytes)
    result = poller.result()
    lines = [line.content for page in result.pages for line in page.lines]
    text = "\n".join(lines)
    logger.debug(f"OCR extracted {len(lines)} lines")
    return text

# Generate JSON via Azure OpenAI
def extract_fields(openai_client: AzureOpenAI, ocr_text: str, language: str = "en") -> Dict[str, Any]:
    logger.info("Calling OpenAI for field extraction...")
    # choose model
    model = "gpt-4o"
    schema = get_schema(language)
    # build prompt
    prompt = f"Extract the following fields from the given form text. Return only JSON with keys exactly as in the schema. Use empty string for missing fields.\nSchema: {json.dumps(schema, ensure_ascii=False)}\n\nForm Text:\n{ocr_text}"
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0
    )
    content = response.choices[0].message.content.strip("```").strip("json")
    try:
        data = json.loads(content)
        logger.info("Extracted JSON successfully.")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {e}")
        return schema  # return empty schema for resilience

# Schema definitions
def get_schema(language: str) -> Dict[str, Any]:
    if language == "he":
        return {
            "שם משפחה": "",
            "שם פרטי": "",
            "מספר זהות": "",
            "מין": "",
            "תאריך לידה": {"יום": "", "חודש": "", "שנה": ""},
            "כתובת": {"רחוב": "", "מספר בית": "", "כניסה": "", "דירה": "", "ישוב": "", "מיקוד": "", "תא דואר": ""},
            "טלפון קווי": "",
            "טלפון נייד": "",
            "סוג העבודה": "",
            "תאריך הפגיעה": {"יום": "", "חודש": "", "שנה": ""},
            "שעת הפגיעה": "",
            "מקום התאונה": "",
            "כתובת מקום התאונה": "",
            "תיאור התאונה": "",
            "האיבר שנפגע": "",
            "חתימה": "",
            "תאריך מילוי הטופס": {"יום": "", "חודש": "", "שנה": ""},
            "תאריך קבלת הטופס בקופה": {"יום": "", "חודש": "", "שנה": ""},
            "למילוי ע\"י המוסד הרפואי": {"חבר בקופת חולים": "", "מהות התאונה": "", "אבחנות רפואיות": ""}
        }
    # default English
    return {
        "lastName": "",
        "firstName": "",
        "idNumber": "",
        "gender": "",
        "dateOfBirth": {"day": "", "month": "", "year": ""},
        "address": {"street": "", "houseNumber": "", "entrance": "", "apartment": "", "city": "", "postalCode": "", "poBox": ""},
        "landlinePhone": "",
        "mobilePhone": "",
        "jobType": "",
        "dateOfInjury": {"day": "", "month": "", "year": ""},
        "timeOfInjury": "",
        "accidentLocation": "",
        "accidentAddress": "",
        "accidentDescription": "",
        "injuredBodyPart": "",
        "signature": "",
        "formFillingDate": {"day": "", "month": "", "year": ""},
        "formReceiptDateAtClinic": {"day": "", "month": "", "year": ""},
        "medicalInstitutionFields": {"healthFundMember": "", "natureOfAccident": "", "medicalDiagnoses": ""}
    }

# Basic validation
def validate_data(data: Dict[str, Any], language: str = "en") -> List[str]:
    missing = []
    def recurse(schema: Dict[str, Any], obj: Dict[str, Any], path: str = ""):
        for key, val in schema.items():
            current_path = f"{path}.{key}" if path else key
            if isinstance(val, dict):
                recurse(val, obj.get(key, {}), current_path)
            else:
                if not obj.get(key):
                    missing.append(current_path)
    recurse(get_schema(language), data)
    return missing

# Streamlit UI
def main():
    st.title("National Insurance Form Extractor")
    st.markdown("Upload a PDF or image of the National Insurance Institute (ביטוח לאומי) form (Hebrew or English). We will extract data to JSON.")
    uploaded_file = st.file_uploader("Choose file", type=["pdf", "jpg", "jpeg"] )
    if not uploaded_file:
        return
    bytes_data = uploaded_file.read()
    # init clients
    form_client, openai_client = init_clients()
    with st.spinner("Running OCR..."):
        ocr_text = analyze_document(form_client, bytes_data)
    st.text_area("OCR Text", ocr_text, height=200)
    # detect language simple heuristic
    lang = "he" if any("שם" in line for line in ocr_text.splitlines()) else "en"
    st.markdown(f"**Detected Language:** {'Hebrew' if lang == 'he' else 'English'}")
    with st.spinner("Extracting fields via OpenAI..."):
        data = extract_fields(openai_client, ocr_text, language=lang)
    st.subheader("Extracted JSON")
    st.json(data)
    missing = validate_data(data, language=lang)
    if missing:
        st.warning("Missing or empty fields:\n" + "\n".join(f"- {field}" for field in missing))
    else:
        st.success("All fields extracted successfully!")

if __name__ == "__main__":
    main()

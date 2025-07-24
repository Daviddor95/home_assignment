from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal, Optional
import logging
import os
import json
import glob
from prompts import (
    info_collection_prompt,
    info_confirmation_prompt,
    qa_prompt,
    extraction_prompt
)
from openai import AzureOpenAI
from dotenv import load_dotenv
from logging_config import configure_logging

# --- Configuration and Initialization ---
configure_logging()
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI(
    title="HMO Information Chatbot API",
    description="This API powers a chatbot to collect user information and answer questions based on their HMO plan.",
    version="1.2.0" 
)

try:
    client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-02-15-preview"
    )
except KeyError as e:
    logger.error(f"Environment variable not set: {e}")
    client = None 

# --- Pydantic Data Models ---
class UserInfo(BaseModel):
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    id_number: str = Field(..., pattern=r"^\d{9}$", description="A 9-digit Israeli ID number")
    gender: Literal["male", "female", "other"] = Field(..., description="User's gender")
    age: int = Field(..., ge=0, le=120, description="User's age, between 0 and 120")
    hmo: Literal["מכבי", "מאוחדת", "כללית"] = Field(..., description="User's HMO")
    card_number: str = Field(..., pattern=r"^\d{9}$", description="A 9-digit HMO card number")
    tier: Literal["זהב", "כסף", "ארד"] = Field(..., description="Insurance tier")

class Message(BaseModel):
    role: Literal["user", "system", "assistant"]
    content: str

class ChatPayload(BaseModel):
    history: List[Message]
    user_info: Optional[UserInfo] = None
    language: str = "en"

class QAPayload(BaseModel):
    user_info: UserInfo
    history: List[Message]
    new_message: str
    language: str = "en"

# --- Helper Functions ---
def get_llm_response(messages: List[dict], model: str = "gpt-4o", as_json: bool = False) -> str:
    if not client: raise HTTPException(status_code=500, detail="Azure OpenAI client is not configured.")
    try:
        response_format = {"type": "json_object"} if as_json else {"type": "text"}
        resp = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
        return resp.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Azure OpenAI: {e}")
        raise HTTPException(status_code=500, detail="Failed to get response from LLM.")

def get_all_knowledge_base_content() -> str:
    """
    Load all knowledge base content from all files. Since each file covers 
    a different topic, we need to combine all files for comprehensive coverage.
    """
    kb_dir = "knowledge_base"
    
    # Get all HTML files in the directory
    html_files = glob.glob(os.path.join(kb_dir, "*.html"))
    
    if not html_files:
        raise FileNotFoundError("No HTML files found in knowledge_base directory")
    
    combined_content = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                filename = os.path.basename(file_path)
                
                # Add a header to identify which file this content came from
                combined_content.append(f"\n\n=== KNOWLEDGE BASE FILE: {filename} ===\n")
                combined_content.append(file_content)
                
                logger.info(f"Loaded knowledge base file: {filename}")
                
        except Exception as e:
            logger.warning(f"Failed to load knowledge base file {file_path}: {e}")
            continue
    
    if not combined_content:
        raise FileNotFoundError("No knowledge base files could be loaded")
    
    logger.info(f"Successfully loaded {len(html_files)} knowledge base files")
    return "\n".join(combined_content)

# --- API Endpoints ---
@app.post("/chat")
async def chat(payload: ChatPayload):
    history = [msg.dict() for msg in payload.history]
    lang = payload.language
    extraction_messages = extraction_prompt(history)
    extracted_json_str = get_llm_response(extraction_messages, as_json=True)
    
    try:
        if extracted_json_str.strip().lower() in ["none", "null", "{}"]: raise ValueError("Not enough info.")
        user_info = UserInfo(**json.loads(extracted_json_str))
        logger.info(f"Successfully extracted and validated user info: {user_info.id_number}")
        confirmation_messages = info_confirmation_prompt(user_info, lang)
        confirmation_text = get_llm_response(confirmation_messages)
        return {"phase": "confirming", "assistant": confirmation_text, "user_info": user_info.dict()}

    except (ValueError, ValidationError, json.JSONDecodeError) as e:
        logger.info(f"Could not extract user info yet, continuing conversation. Reason: {e}")
        collection_messages = info_collection_prompt(history, lang)
        assistant_response = get_llm_response(collection_messages)
        return {"phase": "collecting", "assistant": assistant_response, "user_info": None}

@app.post("/ask")
async def ask(payload: QAPayload):
    try:
        # Load all knowledge base content from all topic files
        kb_content = get_all_knowledge_base_content()
            
    except FileNotFoundError as e:
        logger.error(f"Knowledge base files not found: {e}")
        raise HTTPException(
            status_code=404, 
            detail="Knowledge base files not found. Please ensure the knowledge base files are available in the knowledge_base directory."
        )
    except Exception as e:
        logger.error(f"Error reading knowledge base files: {e}")
        raise HTTPException(status_code=500, detail="Failed to read knowledge base files.")

    qa_messages = qa_prompt(
        user_info=payload.user_info,
        history=[msg.dict() for msg in payload.history],
        new_question=payload.new_message,
        knowledge_base=kb_content,
        language=payload.language
    )
    answer = get_llm_response(qa_messages)
    logger.info("Answered question for %s (%s)", payload.user_info.first_name, payload.user_info.id_number)
    return {"assistant": answer}
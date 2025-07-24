from typing import List, Dict, Any

UserInfoDict = Dict[str, Any]

def info_collection_prompt(history: List[Dict], language: str) -> List[Dict]:
    lang_instruction = "Hebrew" if language == "he" else "English"
    return [
        {
            "role": "system",
            "content": f"""You are a friendly assistant for a health insurance provider. Your goal is to collect user information in a natural, conversational way.
- Ask for one piece of information at a time, or two related ones (e.g., first and last name).
- Be polite and friendly.
- The required pieces of information are: first name, last name, 9-digit ID number, gender, age, HMO name (must be one of: מכבי, מאוחדת, כללית), 9-digit HMO card number, and insurance tier (must be one of: זהב, כסף, ארד).
- Keep the entire conversation in {lang_instruction}."""
        }
    ] + history

def extraction_prompt(history: List[Dict]) -> List[Dict]:
    return [
        {
            "role": "system",
            "content": """Review the following conversation and extract the user's information into a JSON object.
The required fields are: `first_name`, `last_name`, `id_number` (9 digits), `gender` ('male', 'female', or 'other'), `age` (0-120), `hmo` ('מכבי', 'מאוחדת', 'כללית'), `card_number` (9 digits), and `tier` ('זהב', 'כסף', 'ארד').
If any piece of information is missing, respond with the word "None"."""
        },
        { "role": "user", "content": f"Here is the conversation history:\n\n{history}"}
    ]

def info_confirmation_prompt(user_info: UserInfoDict, language: str) -> List[Dict]:
    if language == 'he':
        content = (
            f"מעולה, תודה! אנא הקדש/י רגע לאימות הפרטים שלך:\n\n"
            f"**שם מלא**: {user_info.first_name} {user_info.last_name}\n"
            f"**מספר ת.ז**: {user_info.id_number}\n"
            f"**גיל**: {user_info.age}\n"
            f"**מין**: {user_info.gender}\n"
            f"**קופת חולים**: {user_info.hmo}\n"
            f"**מספר כרטיס קופה**: {user_info.card_number}\n"
            f"**רובד ביטוחי**: {user_info.tier}\n\n"
            "האם כל המידע נכון? אנא השב/השיבי 'כן' לאישור, או ציין/צייני את הפרטים שברצונך לשנות."
        )
    else:
        content = (
            f"Great, thank you! Please take a moment to confirm your details:\n\n"
            f"**Full Name**: {user_info.first_name} {user_info.last_name}\n"
            f"**ID Number**: {user_info.id_number}\n"
            f"**Age**: {user_info.age}\n"
            f"**Gender**: {user_info.gender}\n"
            f"**HMO**: {user_info.hmo}\n"
            f"**HMO Card Number**: {user_info.card_number}\n"
            f"**Insurance Tier**: {user_info.tier}\n\n"
            "Is all of this information correct? Please reply with 'Yes' to confirm or provide the details you'd like to change."
        )
    return [{"role": "system", "content": content}]

def qa_prompt(user_info: UserInfoDict, history: List[Dict], new_question: str, knowledge_base: str, language: str) -> List[Dict]:
    lang_instruction = "Hebrew" if language == "he" else "English"
    system_message = (
        f"You are a helpful assistant for members of {user_info.hmo}. "
        f"The user's current insurance tier is: {user_info.tier}. "
        f"Answer the user's questions in {lang_instruction}, based *only* on the information provided in the HTML knowledge base below. "
        "If the answer is not in the knowledge base, state that you do not have that information.\n\n"
        "--- KNOWLEDGE BASE START ---\n"
        f"{knowledge_base}\n"
        "--- KNOWLEDGE BASE END ---"
    )
    messages = [{"role": "system", "content": system_message}]
    messages.extend([{"role": msg['role'], "content": msg['content']} for msg in history])
    messages.append({"role": "user", "content": new_question})
    return messages
import streamlit as st
import requests
import json

# --- Page and Session State Configuration ---
st.set_page_config(
    page_title="HMO Chatbot",
    page_icon="🩺",
    layout="centered"
)

# --- Localization & UI Text ---
TEXTS = {
    "page_title": {"en": "HMO Services Chatbot 🩺", "he": "🩺 צ'אטבוט שירותי בריאות"},
    "lang_selector": {"en": "Language", "he": "שפה"},
    "confirm_info": {"en": "Please review your information above and either confirm or correct it.", "he": "אנא בדוק/בדקי את הפרטים שלך למעלה ואשר/י או תקן/י אותם."},
    "confirm_yes": {"en": "✅ Yes, this is correct", "he": "✅ כן, המידע נכון"},
    "confirm_no": {"en": "❌ No, I need to change something", "he": "❌ לא, אני צריך/ה לתקן"},
    "user_corrected": {"en": "No, I need to make a correction.", "he": "לא, אני צריך/ה לבצע תיקון."},
    "user_confirmed": {"en": "Yes, this is correct.", "he": "כן, המידע נכון."},
    "assistant_confirmed": {"en": "Great! How can I help you today?", "he": "מעולה! איך אני יכול/ה לעזור היום?"},
    "chat_input_collect": {"en": "Please provide your information...", "he": "ספר על עצמך..."},
    "spinner_thinking": {"en": "Thinking...", "he": "חושב..."},
    "welcome_qa": {"en": "Welcome, {name}! You can now ask questions about your HMO plan.", "he": "ברוך/ה הבא/ה, {name}! כעת ניתן לשאול שאלות על תוכנית הבריאות שלך."},
    "chat_input_qa": {"en": "Ask a question about your health services...", "he": "שאל/י שאלה על שירותי הבריאות שלך..."},
    "spinner_searching": {"en": "Searching for an answer...", "he": "מחפש תשובה..."},
    "error_backend_connection": {"en": "Could not connect to the backend: {e}", "he": "לא ניתן היה להתחבר לשרת: {e}"},
    "error_backend_response": {"en": "Received an invalid response from the backend.", "he": "התקבלה תגובה לא תקינה מהשרת."},
    "error_unexpected": {"en": "An unexpected error occurred: {e}", "he": "אירעה שגיאה בלתי צפויה: {e}"},
}

# --- Language and Layout Setup ---
st.sidebar.title(TEXTS["lang_selector"]["en"] + " / " + TEXTS["lang_selector"]["he"])
lang_options = {"English": "en", "עברית": "he"}
selected_lang_name = st.sidebar.radio("", list(lang_options.keys()))

if "lang" not in st.session_state or st.session_state.lang != lang_options[selected_lang_name]:
    st.session_state.lang = lang_options[selected_lang_name]
    # Reset history on language change to avoid confusion
    st.session_state.history = []
    st.session_state.phase = "collecting"
    st.session_state.user_info = None
    st.session_state.pending_info = None

# Apply RTL styles if Hebrew is selected
if st.session_state.lang == 'he':
    st.markdown(
        """<style>
        html, body, [class*="st-"] { direction: rtl; }
        .stTextInput textarea, .stChatInput textarea { direction: rtl; text-align: right; }
        .st-emotion-cache-1f1G2gn { text-align: right; }
        </style>""", unsafe_allow_html=True
    )
else: # Ensure LTR for English
    st.markdown(
        """<style>
        html, body, [class*="st-"] { direction: ltr; }
        </style>""", unsafe_allow_html=True
    )

# --- Session State Initialization ---
if "phase" not in st.session_state: st.session_state.phase = "collecting"
if "history" not in st.session_state: st.session_state.history = []
if "user_info" not in st.session_state: st.session_state.user_info = None 
if "pending_info" not in st.session_state: st.session_state.pending_info = None
if "show_welcome" not in st.session_state: st.session_state.show_welcome = False

API_URL = "http://localhost:8000"
LANG = st.session_state.lang

# --- UI Rendering ---
st.title(TEXTS["page_title"][LANG])

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Phase-Based Logic ---
if st.session_state.phase in ["collecting", "confirming"]:
    if st.session_state.phase == "confirming":
        st.info(TEXTS["confirm_info"][LANG])
        col1, col2 = st.columns(2)
        if col1.button(TEXTS["confirm_yes"][LANG], use_container_width=True):
            st.session_state.user_info = st.session_state.pending_info
            st.session_state.phase = "qa"
            st.session_state.show_welcome = True  # Show welcome message when entering QA phase
            st.session_state.history.append({"role": "user", "content": TEXTS["user_confirmed"][LANG]})
            st.session_state.history.append({"role": "assistant", "content": TEXTS["assistant_confirmed"][LANG]})
            st.rerun()

        if col2.button(TEXTS["confirm_no"][LANG], use_container_width=True):
            st.session_state.phase = "collecting"
            st.session_state.pending_info = None
            st.session_state.history.append({"role": "user", "content": TEXTS["user_corrected"][LANG]})
            with st.spinner(TEXTS["spinner_thinking"][LANG]):
                response = requests.post(f"{API_URL}/chat", json={"history": st.session_state.history, "language": LANG}).json()
                st.session_state.history.append({"role": "assistant", "content": response["assistant"]})
            st.rerun()

    if prompt := st.chat_input(TEXTS["chat_input_collect"][LANG]):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(TEXTS["spinner_thinking"][LANG]):
                try:
                    payload = {"history": st.session_state.history, "language": LANG}
                    res = requests.post(f"{API_URL}/chat", json=payload)
                    res.raise_for_status()
                    response_data = res.json()
                    st.session_state.history.append({"role": "assistant", "content": response_data["assistant"]})
                    if response_data.get("phase") == "confirming":
                        st.session_state.phase = "confirming"
                        st.session_state.pending_info = response_data.get("user_info")
                    st.rerun()
                except requests.exceptions.RequestException as e: st.error(TEXTS["error_backend_connection"][LANG].format(e=e))
                except json.JSONDecodeError: st.error(TEXTS["error_backend_response"][LANG])

elif st.session_state.phase == "qa":
    # Only show welcome message if show_welcome is True
    if st.session_state.show_welcome:
        st.success(TEXTS["welcome_qa"][LANG].format(name=st.session_state.user_info['first_name']))
    
    if prompt := st.chat_input(TEXTS["chat_input_qa"][LANG]):
        # Hide welcome message after first user message in QA phase
        st.session_state.show_welcome = False
        
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(TEXTS["spinner_searching"][LANG]):
                try:
                    payload = {
                        "user_info": st.session_state.user_info,
                        "history": st.session_state.history[:-1],
                        "new_message": prompt,
                        "language": LANG
                    }
                    res = requests.post(f"{API_URL}/ask", json=payload)
                    res.raise_for_status()
                    response_data = res.json()
                    st.session_state.history.append({"role": "assistant", "content": response_data["assistant"]})
                    st.markdown(response_data["assistant"])
                except requests.exceptions.RequestException as e: st.error(TEXTS["error_backend_connection"][LANG].format(e=e))
                except Exception as e: st.error(TEXTS["error_unexpected"][LANG].format(e=e))
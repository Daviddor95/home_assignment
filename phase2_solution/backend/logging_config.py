import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("chatbot.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

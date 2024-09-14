import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
    UPLOAD_FOLDER = 'uploads/'
    PROCESSED_FOLDER = 'processed/'

config = Config()

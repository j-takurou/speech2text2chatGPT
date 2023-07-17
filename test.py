import openai
import os
openai.api_key = os.getenv("OPENAI_APIKEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config.json"
from sample_speech2text import response_chatGPT


def main():
    response_chatGPT(message="testです。")
    

if __name__ == "__main__":
    main()


import os
import json
import requests
from loguru import logger
from dotenv import load_dotenv


load_dotenv()


NGROK_ENDPOINT = os.getenv("NGROK_ENDPOINT")
HEADER = {"Content-Type": "application/json"}


def chat_vllm_serving_in_colab(input_message: str):
    input_data = {
        "question": input_message,
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    }
    vllm_serving_endpoint = f"{NGROK_ENDPOINT}/api/v1/generate-response"
    response = requests.post(
        vllm_serving_endpoint,
        json=input_data,
        headers=HEADER
    )
    if response.status_code == 200:
        response_json = json.loads(response.text)
        result = response_json['response']['choices'][0]['message']['content']
        return result
    else:
        logger.error(f"Error in chat_vllm_serving_in_colab: {response.status_code} - {response.text}")
        return None

# if __name__ == "__main__":
#     message = "9.9 or 9.11. Which number is higher than"
#     print(chat_vllm_serving_in_colab(message))
import requests
import logging
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)


class DeepSeekClient:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        """
        Initialize the DeepSeek API client.

        :param api_key: Your DeepSeek API key.
        :param base_url: Base URL for the DeepSeek API (default is v1).
        """
        self.api_key = api_key
        self.base_url = base_url

    def send_message(
        self,
        message: str,
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Send a user role message to the DeepSeek API and get a response.

        :param message: The user's message (string).
        :param model: Model to use (default is "deepseek-chat").
        :param temperature: Sampling temperature (default is 0.7).
        :param max_tokens: Maximum number of tokens to generate (default is 1000).
        :return: API response containing the assistant's reply.
        """
        endpoint = "chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        url = f"{self.base_url}/{endpoint}"

        logger.info(f"Sending message to {url}: {data}")

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise HTTP errors if any
            response_data = response.json()
            logger.info(f"Received response: {response_data}")
            return response_data

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response content: {response.text}")
            raise
        except requests.exceptions.RequestException as err:
            logger.error(f"Request error occurred: {err}")
            raise
        except ValueError as err:
            logger.error(f"Error parsing JSON response: {err}")
            raise
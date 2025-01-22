# chat/views.py
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from deepseek_api.api.serializers.deepseek import DeepSeekChatSerializer
from deepseek_api.client import DeepSeekClient  
from django.conf import settings
import requests

class DeepSeekChatViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = DeepSeekChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        message = serializer.validated_data["message"]
        model = serializer.validated_data.get("model", "deepseek-chat")
        temperature = serializer.validated_data.get("temperature", 0.7)
        max_tokens = serializer.validated_data.get("max_tokens", 1000)

        # Initialize DeepSeekClient
        api_key = settings.DEEPSEEK_API_KEY  # Use API key from Django settings
        client = DeepSeekClient(api_key)

        try:
            # Send message to DeepSeek API
            response = client.send_message(
                message=message,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return Response(response, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors (e.g., 4xx, 5xx)
            error_message = str(http_err)
            status_code = http_err.response.status_code if hasattr(http_err, "response") else status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response({"detail": error_message}, status=status_code)

        except requests.exceptions.ConnectionError as conn_err:
            # Handle connection errors (e.g., network issues)
            return Response({"detail": "Connection error: Unable to reach the DeepSeek API."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout as timeout_err:
            # Handle timeout errors
            return Response({"detail": "Request timed out: The DeepSeek API did not respond in time."}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.exceptions.RequestException as req_err:
            # Handle other request-related errors
            return Response({"detail": f"Request error: {str(req_err)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle unexpected errors
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
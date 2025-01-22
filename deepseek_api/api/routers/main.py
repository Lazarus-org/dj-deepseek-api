# chat/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from deepseek_api.api.views.deepseek import DeepSeekChatViewSet

router = DefaultRouter()
router.register(r"deepseek_chat", DeepSeekChatViewSet, basename="deepseek_chat")

urlpatterns = router.urls
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DeepseekApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "deepseek_api"
    verbose_name = _("Django DeepSeek Api")

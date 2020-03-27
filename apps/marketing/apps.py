from django.apps import AppConfig


class MarketingConfig(AppConfig):
    name = 'marketing'
    verbose_name = "营销管理"
    def ready(self):
        import marketing.signals
from django.apps import AppConfig


class FanBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fan_board'

    def ready(self):
        import fan_board.signals

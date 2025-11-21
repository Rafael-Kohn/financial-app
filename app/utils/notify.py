from kivy.clock import Clock
from ..widgets.notification_widget import NotificationWidget

class Notify:
    container = None  # será configurado pelo MainApp

    COLORS = {
        "notice": [0.1, 0.4, 1, 1],   # azul
        "warning": [1, 0.7, 0.1, 1], # amarelo
        "error": [1, 0.2, 0.2, 1],   # vermelho
    }

    @classmethod
    def setup(cls, container):
        cls.container = container

    @classmethod
    def push(cls, level,message ):
        if not cls.container:
            print("Notify não configurado!")
            return

        color = cls.COLORS.get(level, cls.COLORS["notice"])

        def _add(dt):
            notif = NotificationWidget(message=message, bg_color=color)
            cls.container.add_widget(notif)

        Clock.schedule_once(_add, 0)

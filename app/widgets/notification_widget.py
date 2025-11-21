from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock

class NotificationWidget(BoxLayout):
    message = StringProperty("")
    bg_color = ListProperty([0, 0, 0, 1])
    duration = NumericProperty(3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.dismiss, self.duration)

    def dismiss(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

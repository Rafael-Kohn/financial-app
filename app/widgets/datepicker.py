# components/datepicker.py
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
import calendar
from datetime import datetime
from kivy.uix.scrollview import ScrollView

class DatePicker(Popup):
    month = NumericProperty()
    year = NumericProperty()
    month_name = StringProperty()
    callback = ObjectProperty(None)

    def __init__(self, callback=None, **kwargs):
        # callback agora opcional
        super().__init__(**kwargs)
        self.callback = callback

        hoje = datetime.today()
        self.month = hoje.month
        self.year = hoje.year

        self.title = "Selecione a Data"
        self.size_hint = (0.9, 0.8)
        self.auto_dismiss = False

        # content do popup
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.content = self.layout

        # build inicial
        self.refresh()

    def update_month_name(self):
        self.month_name = f"{calendar.month_name[self.month]}"
        self.year_name = f"{self.year}"

    def build_header(self):
        header = GridLayout(cols=3, spacing=5, size_hint_y=None)

        header.add_widget(Button(text="<<", on_release=lambda x: self.prev_year()))
        header.add_widget(Button(text=self.year_name, background_normal='', disabled=True))
        header.add_widget(Button(text=">>", on_release=lambda x: self.next_year()))

        header.add_widget(Button(text="<", on_release=lambda x: self.prev_month()))
        header.add_widget(Button(text=self.month_name, background_normal='', disabled=True))
        header.add_widget(Button(text=">", on_release=lambda x: self.next_month()))
        

        return header

    def build_calendar(self):
        scroll = ScrollView(size_hint=(1, 1))

        grid = GridLayout(cols=7, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        # nomes dias
        for d in ["D", "S", "T", "Q", "Q", "S", "S"]:
            btn = Button(text=d, size_hint_y=None, height=40, disabled=True)
            grid.add_widget(btn)

        month_calendar = calendar.monthcalendar(self.year, self.month)
        for week in month_calendar:
            for day in week:
                if day == 0:
                    grid.add_widget(Button(text="", disabled=True, size_hint_y=None, height=40))
                else:
                    grid.add_widget(
                        Button(
                            text=str(day),
                            on_release=lambda x, d=day: self.select_day(d),
                            size_hint_y=None,
                            height=40,
                        )
                    )

        scroll.add_widget(grid)
        return scroll

    def prev_month(self):
        self.month -= 1
        if self.month <= 0:
            self.month = 12
            self.year -= 1
        self.refresh()

    def next_month(self):
        self.month += 1
        if self.month >= 13:
            self.month = 1
            self.year += 1
        self.refresh()

    def prev_year(self):
        self.year -= 1
        self.refresh()

    def next_year(self):
        self.year += 1
        self.refresh()

    def refresh(self):
        # reconstrói content inteiro
        self.layout.clear_widgets()
        self.update_month_name()
        self.layout.add_widget(self.build_header())
        self.layout.add_widget(self.build_calendar())

    def select_day(self, day):
        data = f"{day:02d}/{self.month:02d}/{self.year}"
        if callable(self.callback):
            self.callback(data)
        self.dismiss()

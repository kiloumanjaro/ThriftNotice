import flet as ft

class Preference(ft.View):
    def __init__(self, page: ft.Page): 
        super(Preference, self).__init__(route="/preference")
        self.page = page

        questions_content = ft.Container(
            width=375,
            height=575,
            padding=10,
            content=ft.Text(value="Questions"),  # Fixed text syntax
        )

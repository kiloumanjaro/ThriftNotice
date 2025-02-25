import flet as ft

class Landing(ft.View):
    def __init__(self, page: ft.Page): 
        super(Landing, self).__init__(
            route="/", horizontal_alignment="center",
            vertical_alignment="center"
        )

        self.page = page

        self.tab_logo = ft.Icon(name="shopping_cart_outlined", size=200)    
        self.title = ft.Text("Thrift Notice", size=28, weight="bold", text_align="center")

        # Column to control spacing between logo and title, ensuring center alignment
        self.logo_title_column = ft.Column([
            self.tab_logo,
            ft.Container(height=10),  # Adjust height for spacing
            self.title
        ], alignment="center", horizontal_alignment="center", spacing=20)

        # Get Started Button
        self.get_started_button = ft.ElevatedButton(
            text="Get Started",
            on_click=lambda e: self.page.go("/maps"),
            width=200
        )

        self.controls = [
            ft.Column([
                self.logo_title_column, 
                ft.Divider(height=10, color="transparent"),
                ft.Container(
                    content=self.get_started_button,
                    alignment=ft.alignment.center,
                    expand=True
                )  # Button sticks to the bottom
            ], alignment="center", horizontal_alignment="center", expand=True)
        ]

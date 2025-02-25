import flet as ft

class Landing(ft.View):
    def __init__(self, page: ft.Page): 
        super(Landing, self).__init__(
            route="/", horizontal_alignment="center",
            vertical_alignment="center"
        )

        self.page = page

        # Logo Image
        self.logo = ft.Container(
            content=ft.Image(src="thrift.png", width=280, height=280),
            bgcolor="white"
        )

        # Column to control spacing between logo and title, ensuring center alignment
        self.logo_title_column = ft.Column([
            self.logo,  # Add logo above the title
            ft.Container(height=10),  # Adjust height for spacing
            ft.Text("Thrift Notice", size=28, weight="bold", text_align="center"),
            ft.Text("The art of thrifting isn’t for everyone, but we just might change your mind.", size=13, text_align="center")
        ], alignment="center", horizontal_alignment="center")

        # Get Started Button
        self.get_started_button = ft.ElevatedButton(
            text="Get Started",
            on_click=lambda e: self.page.go("/maps"),
            width=200, 
            height=50, 
            style=ft.ButtonStyle(
                bgcolor="#1c1c1c",  # Background color
                color="white",  # Text color
                elevation=0  # Remove shadow effect
            )
        )

        self.controls = [
            ft.Container(
                expand=True,
                padding=ft.padding.only(left=30, right=30),
                bgcolor="white",
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Divider(height=25, color="transparent"),
                        self.logo_title_column, 
                        ft.Divider(height=10, color="transparent"),
                        ft.Container(
                            padding=ft.padding.only(left=20, right=20, top=0, bottom=25),
                            alignment=ft.alignment.bottom_center,
                            content=self.get_started_button
                        )  # Button sticks to the bottom
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Pushes button to the bottom
                )
            )
        ]

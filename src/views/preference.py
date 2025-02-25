import flet as ft

class Preference(ft.View):

    def __init__(self, page: ft.Page): 
        super(Preference, self).__init__(route="/preference")
        self.page = page
        self.initialize()

    def initialize(self):
        self.controls = [self.display_questionaire_container()]
    
    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def display_questionaire_container(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=15,
                controls=[
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Back",
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back_to_maps,
                                style=ft.ButtonStyle(
                                    shape={"": ft.RoundedRectangleBorder(radius=25)},
                                    padding=ft.padding.symmetric(vertical=10, horizontal=20),
                                    bgcolor="white",
                                    color="black",
                                )
                            ),
                        ],
                        alignment="start",  # Align to the left
                    ),
                    ft.Container(
                        expand=True,  # Ensures full space usage
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Shopping Preferences", 
                                    size=20, 
                                    weight="bold"
                                ),
                                ft.Container(height=3),
                                # Wrap both Text and Dropdown inside a Column
                                ft.Container(
                                    padding=ft.padding.only(left=20),  # Apply padding here
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Clothing",
                                                size=14
                                            ),
                                            ft.Dropdown(
                                                hint_text="Select your clothing style",
                                                width=300,
                                                text_style=ft.TextStyle(size=11, color="gray"),  # Change hint_text size
                                                options=[
                                                    ft.dropdown.Option("Casual wear"),
                                                    ft.dropdown.Option("Vintage pieces"),
                                                    ft.dropdown.Option("Formal attire"),
                                                    ft.dropdown.Option("Streetwear"),
                                                    ft.dropdown.Option("Designer/Branded items"),
                                                ]
                                            ),
                                            ft.Container(height=2),
                                            
                                            ft.Text(
                                                "Budget",
                                                size=14
                                            ),
                                            ft.Dropdown(
                                                hint_text="What is your preferred price range per item?",
                                                width=300,
                                                text_style=ft.TextStyle(size=11, color="gray"),  # Change hint_text size
                                                options=[
                                                    ft.dropdown.Option("Below 50"),
                                                    ft.dropdown.Option("50-150"),
                                                    ft.dropdown.Option("150-300"),
                                                    ft.dropdown.Option("300-500"),
                                                    ft.dropdown.Option("500+"),
                                                ]
                                            ),
                                            ft.Container(height=2),

                                            ft.Text(
                                                "Shopping Environment",
                                                size=14
                                            ),
                                            ft.Dropdown(
                                                hint_text="Do you prefer stores with air conditioning?",
                                                width=300,
                                                text_style=ft.TextStyle(size=11, color="gray"),  # Change hint_text size
                                                options=[
                                                    ft.dropdown.Option("Yes"),
                                                    ft.dropdown.Option("No"),
                                                    ft.dropdown.Option("No preference"),
                                                ]
                                            ),
                                            ft.Container(height=2),

                                            ft.Text(
                                                "Organization",
                                                size=14
                                            ),
                                            ft.Dropdown(
                                                hint_text="Do you enjoy thrift stores that are:",
                                                width=300,
                                                text_style=ft.TextStyle(size=11, color="gray"),  # Change hint_text size
                                                options=[
                                                    ft.dropdown.Option("Open spaced and free-flowing"),
                                                    ft.dropdown.Option("Well-organized and categorized"),
                                                    ft.dropdown.Option("More of a “treasure hunt” style"),
                                                    ft.dropdown.Option("No preference"),
                                                ]
                                            ),
                                            ft.Container(height=2),
                                            ft.Text(
                                                "Interest",
                                                size=14
                                            ),
                                            ft.Dropdown(
                                                hint_text="Are you interested in stores that specialize in:",
                                                width=300,
                                                text_style=ft.TextStyle(size=11, color="gray"),  # Change hint_text size
                                                options=[
                                                    ft.dropdown.Option("Sustainable and eco-friendly fashion"),
                                                    ft.dropdown.Option("Rare or collectors items"),
                                                    ft.dropdown.Option("High-end secondhand fashion"),
                                                    ft.dropdown.Option("Budget-friendly bulk buys"),
                                                ]
                                            ),
                                            ft.Container(height=2),
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                ]
        )
    )
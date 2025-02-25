import flet as ft

class About(ft.View):

    def __init__(self, page: ft.Page): 
        super(About, self).__init__(route="/about")
        self.page = page
        self.initialize()

    def initialize(self):
        self.controls = [self.display_about_container()]

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def display_about_container(self): 
        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    # Back Button (Top-Left)
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
                        padding=ft.padding.only(left=20, right=20),
                        expand=True,  # Ensures full space usage
                        alignment=ft.alignment.center,  # Centers the content
                        content=ft.Column(
                            alignment="center",
                            horizontal_alignment="center",
                            controls=[
                                ft.Text("ABOUT", size=24, weight="bold"),
                                ft.Text(
                                    "This project aims to develop a comprehensive application that helps users locate ukay-ukay "
                                    "(thrift stores) and pop-up shops by leveraging AI and geolocation technologies. The system will "
                                    "extract relevant location details from social media posts and marketplace listings, summarize "
                                    "them using GPT AI, and map them accurately with a geocoding API. This ensures users receive concise, "
                                    "relevant information and can easily visualize shop locations on an interactive map. With a user-friendly "
                                    "interface and real-time updates, the app streamlines the discovery of affordable fashion and unique "
                                    "finds while supporting small businesses and sustainable shopping.",
                                    size=14,
                                    text_align="center",
                                ),
                            ]
                        ),
                    ),
                ]
            )
        )
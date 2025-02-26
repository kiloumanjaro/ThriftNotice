import flet as ft

class About(ft.View):

    def __init__(self, page: ft.Page): 
        super(About, self).__init__(route="/about", padding=0, bgcolor="#1c1c1c")
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
                spacing=2,  # Manual spacing between elements
                controls=[
                    ft.Container(
                        padding=10,
                        content = ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    on_click=self.go_back_to_maps,
                                    style=ft.ButtonStyle(
                                        shape={"": ft.CircleBorder()},
                                        padding=ft.padding.all(5),
                                        bgcolor="#1c1c1c",
                                        color="white",
                                    )
                                ),
                                ft.Container(
                                    padding=ft.padding.only(left=96),
                                    content=ft.Text("About", size=16, weight=ft.FontWeight.BOLD, color="white"),
                                    alignment=ft.alignment.center
                                ),
                            ],
                            alignment="start",
                        ),
                    ),
                    # Main Content
                    ft.Container(height=8), #SPACE
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,  # Centers horizontally
                        controls=[
                            ft.Container(
                                bgcolor="#1c1c1c",
                                content=ft.Image(src="thrift2.png", width=250, height=250),
                            ),
                        ],
                    ),
                    ft.Container(height=20), #SPACE
                    ft.Container(
                        border_radius=ft.border_radius.only(top_left=30, top_right=30),
                        bgcolor="white",
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            alignment="center",
                            horizontal_alignment="center",
                            spacing=1,  # Manual spacing between text elements
                            controls=[
                                # Title
                                ft.Text(
                                    "Thrift Notice", 
                                    size=24, 
                                    weight="bold",
                                    color="black",  
                                ),

                                ft.Container(
                                    bgcolor="white",
                                    padding=ft.padding.only(left=30, right=30, top=12, bottom=20),
                                    content=ft.Text(
                                        "Thrift Notice collates thrift stores all over Cebu from community input and matches its users to the most compatible stores depending on what they're looking for. Thrift Notice aims to lower the bar of entry for new thrifters and to promote sustainable thrift culture in the contemporary backdrop of Fast Fashion.",
                                        size=12,
                                        text_align="center",
                                        color="black",
                                    ),
                                ),

             
                                # FOOTER SECTION
                                ft.Container(
                                    padding=ft.padding.only(top=7),  
                                    alignment=ft.alignment.center,
                                    content=ft.Column(
                                        alignment="center",
                                        horizontal_alignment="center",
                                        spacing=2,  # Manual spacing between footer sections
                                        controls=[
                                            ft.Text(
                                                "Contact Us",
                                                weight="bold", 
                                                size=11, 
                                                color="#606060",
                                            ),

                                            # Contact Details
                                            ft.Column(
                                                spacing=1,  
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text("Mobile No.:", size=9, color="#606060"),
                                                            ft.Text("+1234567890", size=9, color="#606060")
                                                        ],
                                                        alignment="center"
                                                    ),
                                                    
                                                    ft.Row(
                                                        controls=[
                                                            ft.Text("Email:", size=9, color="#606060"),
                                                            ft.Text("TBA@gmail.com", size=9, color="#606060")
                                                        ],
                                                        alignment="center"
                                                    ),
                                                ],
                                                alignment="center",
                                                horizontal_alignment="center"
                                            ),
                                        ]
                                    )
                                ),
                            ]
                        ),
                    ),
                ]
            )
        )

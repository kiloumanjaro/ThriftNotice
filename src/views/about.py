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
            bgcolor="white",  # White background
            padding=ft.padding.symmetric(horizontal=20),  # Standard padding applied
            content=ft.Column(
                expand=True,
                spacing=2,  # Manual spacing between elements
                controls=[
                    # Back Button
                    ft.Container(
                        margin=ft.margin.only(top=20),
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    on_click=self.go_back_to_maps,
                                    icon_color="black",  
                                    bgcolor="white",
                                    style=ft.ButtonStyle(
                                        shape=None,  
                                        padding=ft.padding.all(10),  # Keeps button spacing
                                    )
                                ),
                            ],
                            alignment="start",
                        ),
                    ),
                    
                    # Main Content
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            alignment="center",
                            horizontal_alignment="center",
                            spacing=2,  # Manual spacing between text elements
                            controls=[
                                # Title
                                ft.Text(
                                    "Hey Thrifters!", 
                                    size=24, 
                                    weight="bold",
                                    color="#606060",  
                                ),

                                # Description
                                ft.Text(
                                    "Discover hidden thrift store gems and pop-up shops near you! Our app simplifies the search for "
                                    "affordable fashion by leveraging AI and real-time location tracking.",
                                    size=12,
                                    text_align="center",
                                    color="#606060",
                                ),

                                ft.Container(height=15), #SPACE

                                # About Section
                                ft.Text(
                                    "About", 
                                    size=18, 
                                    weight="bold", 
                                    color="#606060",
                                ),

                                ft.Text(
                                    "This app leverages AI and geolocation to help users discover thrift stores and pop-up shops. "
                                    "By analyzing social media and marketplace listings, it provides concise, real-time information "
                                    "and an interactive map for a seamless shopping experience.",
                                    size=10,
                                    text_align="center",
                                    color="#606060",
                                ),

                                 ft.Container(height=50), #SPACE

                                # Team Introduction
                                ft.Text(
                                    "Meet Our Team", 
                                    size=16, 
                                    weight="regular", 
                                    color="#606060",
                                ),
                    
                                ft.Text(
                                    "TBA is a passionate group of developers, designers, and thrift enthusiasts dedicated to revolutionizing the way you shop.",
                                    size=10,
                                    text_align="center",
                                    color="#606060",
                                ),

                                ft.Container(height=20), #SPACE

             
                                # FOOTER SECTION
                                ft.Container(
                                    padding=ft.padding.only(top=20),  
                                    alignment=ft.alignment.center,
                                    content=ft.Column(
                                        alignment="center",
                                        horizontal_alignment="center",
                                        spacing=2,  # Manual spacing between footer sections
                                        controls=[
                                            ft.Text(
                                                "Join Our Community Now!", #call
                                                size=10,
                                                weight="bold",
                                                color="#606060",
                                            ),

                                            ft.Text(
                                                "Contact Us", 
                                                size=14, 
                                                weight="bold", 
                                                color="#606060",
                                            ),

                                            # Contact Details
                                            ft.Column(
                                                spacing=2,  
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

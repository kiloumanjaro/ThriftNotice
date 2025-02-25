import flet as ft

class Create(ft.View):

    def __init__(self, page: ft.Page): 
        super(Create, self).__init__(route="/create")
        self.page = page
        self.initialize()

    
    def initialize(self):
        self.controls = [self.display_create_container()]

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()
    
    def display_create_container(self):
        name = ft.TextField()
        address = ft.TextField(multiline=True, max_lines=2)
        
        type_selector = ft.Dropdown(
            options=[
                ft.dropdown.Option("Pop-up"),
                ft.dropdown.Option("Store")
            ]
        )

        date_time_field = ft.TextField(disabled=True, width=155)

        def on_type_change(e):
            date_time_field.disabled = type_selector.value != "Pop-up"
            self.page.update()

        type_selector.on_change = on_type_change

        submit_button = ft.Row(
            alignment="center",  # Center horizontally
            controls=[
                ft.ElevatedButton(
                    "Submit", 
                    on_click=lambda e: print("Form Submitted"),
                    width=200,  # Adjust the width as needed
                    height=50,  # Adjust the height as needed
                    style=ft.ButtonStyle(
                        bgcolor="#1c1c1c",  # Background color
                        color="white",  # Text color
                        elevation=0  # Remove shadow effect
                    )
                )
            ]
        )

        bg='#1c1c1c'
        fg='#98e2f6'
        wg='#f8f9ff'
        fg1='#5f82a6'

        return ft.Container(
            expand=True,
            bgcolor='white',
            content=ft.Column(
                expand=True,
                controls=[  
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back_to_maps,
                                style=ft.ButtonStyle(
                                    shape={"": ft.CircleBorder()},
                                    padding=ft.padding.all(5),
                                    bgcolor="white",
                                    color="black",
                                )
                            ),
                            ft.Container(
                                padding=ft.padding.only(left=70),
                                content=ft.Text("Add Location", size=16, weight=ft.FontWeight.BOLD),
                                alignment=ft.alignment.center
                            ),
                        ],
                        alignment="start",
                    ),
                    ft.Container(
                        padding=ft.padding.only(top=0, left=10, right=10, bottom=0),
                        alignment=ft.alignment.bottom_center,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.MAP, color=fg1, size=180),  # Added landmark icon
                            ],
                            alignment="center"
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, top=0, bottom=25),
                        content=ft.Column(
                            controls=[
                                ft.Text("Title", size=13),
                                name,
                                ft.Text("Address", size=13),
                                address,
                                ft.Text("Type                                Date & Time", size=13),
                                ft.Row(  
                                    controls=[
                                        type_selector,
                                        date_time_field
                                    ],
                                    alignment="stretch"
                                ),
                                ft.Divider(height=15, color="transparent"),
                                submit_button
                            ]
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Pushes the placeholder to the bottom
            )
        )


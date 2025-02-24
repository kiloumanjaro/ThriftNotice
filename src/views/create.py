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
        description = ft.TextField(multiline=True, max_lines=2)
        
        type_selector = ft.Dropdown(
            options=[
                ft.dropdown.Option("Pop-up"),
                ft.dropdown.Option("Store")
            ]
        )

        date_time_field = ft.TextField(disabled=True)

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
                        color="black"  # Change this to any color you want
                    )
                )
            ]
        )

        return ft.Container(
            expand=True,
            bgcolor='white',
            content=ft.Column(
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
                    ft.Divider(height=10, color="transparent"),
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, top=0),
                        content=ft.Column(
                            controls=[
                                ft.Divider(height=10, color="transparent"),
                                ft.Text("Title", size=13),
                                name,
                                ft.Text("Description", size=13),
                                description,
                                ft.Divider(height=15, color="transparent"),
                                ft.Text("Type", size=13),
                                type_selector,
                                ft.Divider(height=5, color="transparent"),
                                ft.Text("Date & Time", size=13),
                                date_time_field,
                                ft.Divider(height=15, color="transparent"),
                                submit_button  # Now centered
                            ]
                        )
                    )
                ]
            )
        )

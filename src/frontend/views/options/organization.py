import flet as ft

def organization_page(pref_view):
    selected_organization = ft.Ref[ft.Text]()  # Stores selected organization preference

    def select_organization(e):
        selected_organization.current.value = e.control.text
        selected_organization.current.update()

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=20),  
        content=ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                ft.Text("Sorting preferences.", size=20, weight="bold", text_align="center"),
                
                ft.Container(height=20), 
                
                ft.Text(
                    "How do you prefer the clothes to be organized?", 
                    size=14, 
                    color=ft.colors.GREY,
                    text_align="center"
                ),

                ft.Container(height=20),  

                # Organization choices as outlined buttons
                ft.Column(
                    spacing=10,
                    controls=[
                        ft.OutlinedButton(
                            text="By color",
                            on_click=select_organization,
                            width=300,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="By category",
                            on_click=select_organization,
                            width=300,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="By season",
                            on_click=select_organization,
                            width=300,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="No specific organization",
                            on_click=select_organization,
                            width=300,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                    ],
                    alignment="center"
                ),

                ft.Container(height=30),  
                
                # Navigation buttons
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.ElevatedButton(
                            text="Previous",
                            on_click=pref_view.prev_page,
                            width=120,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
                        ),
                        ft.ElevatedButton(
                            text="Next",
                            on_click=pref_view.next_page,
                            width=120,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
                        ),
                    ]
                ),
            ]
        )
    )

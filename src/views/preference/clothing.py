import flet as ft

def clothing_page(pref_view):
    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                # Title and Subtitle
                ft.Text("Help us help you.", size=20, weight="bold", text_align="center"),
                ft.Container(height=20),
                ft.Text(
                    "Which type of clothing catches your eye today?", 
                    size=14, 
                    text_align="center", 
                    color=ft.colors.GREY  
                ),
                
                ft.Container(height=20),  
                
                # Checkbox options 
                ft.Column(
                    spacing=10,
                    controls=[
                        ft.OutlinedButton(
                            text="Casual wear", 
                            on_click=None, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)  
                            )
                        ),
                        ft.OutlinedButton(
                            text="Vintage pieces", 
                            on_click=None, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="Formal attire", 
                            on_click=None, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="Streetwear", 
                            on_click=None, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="Designer/Branded items", 
                            on_click=None, 
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
                            on_click=pref_view.go_back_to_maps,
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

import flet as ft

def interest_page(pref_view):
    selected_interest = ft.Ref[ft.Text]()  # Stores selected interest

    def select_interest(e):
        selected_interest.current.value = e.control.text
        selected_interest.current.update()

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                # Title and Subtitle
                ft.Text("Fuel your fashion interest!", size=20, weight="bold", text_align="center"),
                ft.Container(height=20),
                ft.Text(
                    "What sparks your fashion curiosity?", 
                    size=14, 
                    text_align="center", 
                    color=ft.colors.GREY  
                ),
                
                ft.Container(height=20), 
                
                # Interest choices
                ft.Column(
                    spacing=10,
                    controls=[
                        ft.OutlinedButton(
                            text="Fashion trends", 
                            on_click=select_interest, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)  
                            )
                        ),
                        ft.OutlinedButton(
                            text="Sustainable clothing", 
                            on_click=select_interest, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="DIY fashion", 
                            on_click=select_interest, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="Designer pieces", 
                            on_click=select_interest, 
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
                            text="Finish",
                            on_click=pref_view.go_back_to_maps,
                            width=120,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
                        ),
                    ]
                ),
            ]
        )
    )

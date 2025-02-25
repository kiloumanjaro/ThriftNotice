import flet as ft

def budget_page(pref_view):
    selected_budget = ft.Ref[ft.Text]()  # Stores selected budget range

    def select_budget(e):
        selected_budget.current.value = e.control.text
        selected_budget.current.update()

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                # Title and Subtitle
                ft.Text("Let's thrift!", size=20, weight="bold", text_align="center"),
                ft.Container(height=20),
                ft.Text(
                    "What's your ideal price range for that fabulous find?", 
                    size=14, 
                    text_align="center", 
                    color=ft.colors.GREY  
                ),
                
                ft.Container(height=20),  
                
                # Budget choices 
                ft.Column(
                    spacing=10,
                    controls=[
                        ft.OutlinedButton(
                            text="Below $10", 
                            on_click=select_budget, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="$10 - $50", 
                            on_click=select_budget, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="$50 - $100", 
                            on_click=select_budget, 
                            width=300, 
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ),
                        ft.OutlinedButton(
                            text="Above $100", 
                            on_click=select_budget, 
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
                            on_click=pref_view.prev_page,  # ✅ Correct method call
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

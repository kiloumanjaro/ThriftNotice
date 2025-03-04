import flet as ft

def budget_page(pref_view):
    # Reference for displaying selected budget
    selected_budget = ft.Ref[ft.Text]()

    def select_budget(e):
        pref_view.update_preference("budget", e.control.data)  # Save preference
        selected_budget.current.value = f"Selected: {e.control.data}"
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
                    "What is your preferred price range per item?", 
                    size=14, 
                    text_align="center", 
                    color=ft.colors.GREY  
                ),
                
                ft.Container(height=20),  
                
                # Budget choices 
                ft.Column(
                    spacing=10,
                    alignment="center",
                    controls=[
                        ft.OutlinedButton(
                            text=option, 
                            data=option,  # Store option data
                            on_click=select_budget, 
                            width=300, 
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ) for option in ["Below ₱50", "₱50 - ₱150", "₱150 - ₱300", "₱300 - ₱500", "₱500+"]
                    ]
                ),

                ft.Container(height=20),  
                
                # Display selected budget
                ft.Text(ref=selected_budget, size=14, italic=True, color=ft.colors.GREY),

                ft.Container(height=30),  
                
                # Navigation buttons
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.ElevatedButton(
                            text="Previous",
                            on_click=lambda e: pref_view.set_page(1),  # Explicit page navigation
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

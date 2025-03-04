import flet as ft

def clothing_page(pref_view):
    # Reference for displaying selected budget
    selected_clothing = ft.Ref[ft.Text]()

    def select_clothing(e):
        pref_view.update_preference("clothing", e.control.data)  # Save preference
        selected_clothing.current.value = f"Selected: {e.control.data}"
        selected_clothing.current.update()

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
                
                # Clothing choices as outlined buttons
                ft.Column(
                    spacing=10,
                    alignment="center",
                    controls=[
                        ft.OutlinedButton(
                            text=option, 
                            data=option,
                            on_click=select_clothing,
                            width=300, 
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ) for option in [
                            "Casual wear", "Vintage pieces", "Formal attire", 
                            "Streetwear", "Designer/Branded items"
                        ]
                    ]
                ),
                
                ft.Container(height=20),  
                
                # Display selected clothing types
                ft.Text(ref=selected_clothing, size=14, italic=True, color=ft.colors.GREY),

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

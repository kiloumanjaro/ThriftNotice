import flet as ft

def clothing_page(pref_view):
    selected_clothing = ft.Ref[ft.Text]()  # Stores selected clothing types
    selected_options = set()  # Tracks selected options

    def toggle_clothing(e):
        option = e.control.data  # Retrieve option text
        if option in selected_options:
            selected_options.remove(option)
        else:
            selected_options.add(option)

        # Save preferences and update UI
        pref_view.update_preference("clothing_types", list(selected_options))
        selected_clothing.current.value = f"Selected: {', '.join(selected_options) if selected_options else 'None'}"
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
                            on_click=toggle_clothing,
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

import flet as ft

def interest_page(pref_view):
    selected_interest = ft.Ref[ft.Text]()  # Stores selected interests
    selected_options = set()  # Tracks selected interests

    def toggle_interest(e):
        option = e.control.data  # Retrieve option text
        if option in selected_options:
            selected_options.remove(option)
        else:
            selected_options.add(option)

        # Save preferences and update UI
        pref_view.update_preference("fashion_interests", list(selected_options))
        selected_interest.current.value = f"Selected: {', '.join(selected_options) if selected_options else 'None'}"
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
                
                # Interest choices as outlined buttons
                ft.Column(
                    spacing=10,
                    alignment="center",
                    controls=[
                        ft.OutlinedButton(
                            text=option, 
                            data=option,
                            on_click=toggle_interest,
                            width=300, 
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ) for option in [
                            "Fashion trends", "Sustainable clothing", 
                            "DIY fashion", "Designer pieces"
                        ]
                    ]
                ),

                ft.Container(height=20),  
                
                # Display selected interests
                ft.Text(ref=selected_interest, size=14, italic=True, color=ft.colors.GREY),

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

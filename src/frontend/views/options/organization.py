import flet as ft

def organization_page(pref_view):
    # Reference for displaying selected organization preference
    selected_organization = ft.Ref[ft.Text]()

    def select_organization(e):
        pref_view.update_preference("organization", e.control.data)  # Save preference
        selected_organization.current.value = f"Selected: {e.control.data}"
        selected_organization.current.update()

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=20),  
        content=ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                # Title and Subtitle
                ft.Text("Sorting Preferences", size=20, weight="bold", text_align="center"),
                ft.Container(height=20), 
                ft.Text(
                    "Do you enjoy thrift stores that are:", 
                    size=14, 
                    color=ft.colors.GREY,
                    text_align="center"
                ),

                ft.Container(height=20),  

                # Organization choices as outlined buttons
                ft.Column(
                    spacing=10,
                    alignment="center",
                    controls=[
                        ft.OutlinedButton(
                            text=option,
                            data=option,  # Store option data
                            on_click=select_organization,
                            width=300,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                text_style=ft.TextStyle(size=12),
                                side=ft.BorderSide(1, ft.colors.GREY)
                            )
                        ) for option in ["Open spaced and free-flowing", "Well-organized and categorized", 
                                         "More of a “treasure hunt” style", "No preference"]
                    ]
                ),

                ft.Container(height=20),  
                
                # Display selected organization
                ft.Text(ref=selected_organization, size=14, italic=True, color=ft.colors.GREY),

                ft.Container(height=30),  
                
                # Navigation buttons
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.ElevatedButton(
                            text="Previous",
                            on_click=lambda e: pref_view.set_page(2),  # Explicit navigation
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

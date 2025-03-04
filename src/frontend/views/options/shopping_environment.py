import flet as ft

def shopping_environment_page(pref_view):
    # Options for store environment feel
    shopping_options = [
        "Cozy and personal",
        "Trendy and vibrant",
        "Minimalist and modern",
        "Rustic and vintage"
    ]

    # Container to store selected option
    selected_option = ft.Ref[ft.Text]()

    def select_option(e):
        pref_view.update_preference("shopping_environment", e.control.data)
        selected_option.current.value = f"Selected: {e.control.data}"
        selected_option.current.update()

def shopping_environment_page(pref_view):
    # Reference for displaying selected budget
    selected_shopping_env = ft.Ref[ft.Text]()

    def select_shopping_env(e):
        pref_view.update_preference("shoppingenvironment", e.control.data)  # Save preference
        selected_shopping_env.current.value = f"Selected: {e.control.data}"
        selected_shopping_env.current.update()

    return ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                # Title and Subtitle
                ft.Text("Experience your ideal shopping experience!", size=20, weight="bold", text_align="center"),
                ft.Container(height=20),
                ft.Text(
                    "How would you like your store environment to feel?", 
                    size=14, 
                    text_align="center", 
                    color=ft.colors.GREY
                ),

                ft.Container(height=20), 
                
               
                ft.Column(
                    alignment="center",
                    controls=[
                        ft.OutlinedButton(
                            text=option,
                            data=option,
                            on_click=select_shopping_env,
                            width=300,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                text_style=ft.TextStyle(size=12),  
                                side=ft.BorderSide(1, ft.colors.GREY)  
                            )
                        ) for option in [
                                "Cozy and personal",
                                "Trendy and vibrant",
                                "Minimalist and modern",
                                "Rustic and vintage"
                        ]
                    ]
                ),

                ft.Container(height=20),  
                
                # Display selected option
                ft.Text(ref=selected_shopping_env, size=14, italic=True, color=ft.colors.GREY),
                
                ft.Container(height=30), 
                
                # Navigation buttons
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.ElevatedButton(
                            text="Previous",
                            on_click=lambda e: pref_view.set_page(1),  
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

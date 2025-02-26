import flet as ft

class Profile(ft.View):
    def __init__(self, page: ft.Page): 
        super(Profile, self).__init__(
            route="/", horizontal_alignment="center",
            vertical_alignment="center", padding=0,
        )
        self.page = page
        self.wg = '#f8f9ff'
        self.bg = '#1c1c1c'
        self.bg1 = '#323232'
        self.fg='#98e2f6'
        self.bgcolor = self.bg

        # Profile Icon
        self.profile_icon = ft.Container(
            content=ft.Icon(name=ft.icons.FACE, size=200, color="black"),
            bgcolor="white"
        )

        # Profile Container (Title + Icon)
        self.profile_container = ft.Container(
            bgcolor="white", 
            border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
            width=375,
            height=260,
            content=ft.Column(
                controls=[  # Correct placement of the list
                    self.profile_icon,  # Add profile icon above the title
                    #ft.Container(height=15),  # Adjust height for spacing
                    #ft.TextField(label="Who are you?", border="underline"),
                ],
                horizontal_alignment="center",
                alignment="center"
            )
        )


        self.name_container = ft.Container(
            padding=ft.padding.only(left=40, right=40, top=0, bottom=0),
            content=ft.Column(
                controls=[ 
                    ft.Container(
                        bgcolor=self.bg1,  # Match background
                        border_radius=10,  # Rounded corners
                        padding=ft.padding.all(5),  # Add padding to prevent clipping
                        content=ft.TextField(
                            label="Who are you?",
                            border="none",  # Remove default border
                            bgcolor=self.bg1,  # Match container background
                            color="white",  # Text color
                            label_style=ft.TextStyle(color="white"),  # Make label white
                        ),
                    ),
                    ft.Divider(height=30, color="transparent"),
                    ft.Container(
                        padding=ft.padding.only(left=30, right=30),
                        content=ft.Text("Would like AI to assist you?", size=28, text_align="center", color="White")
                    )
                        
                ]    
            )
        )

        # Get Started Button
        self.proceed_button = ft.ElevatedButton(
            text="Proceed",
            on_click=lambda e: self.page.go("/questions"),
            width=190, 
            height=47, 
            style=ft.ButtonStyle(
                bgcolor=self.fg,  # Background color
                color="black",  # Text color
                elevation=0,  # Remove shadow effect
                shape=ft.RoundedRectangleBorder(radius=20),
                text_style=ft.TextStyle(size=13)
            )
        )

        self.skip_button = ft.ElevatedButton(
            text="Skip",
            on_click=lambda e: self.page.go("/maps"),
            width=110, 
            height=47, 
            style=ft.ButtonStyle(
                bgcolor=self.bg1,  # Background color
                color="white",  # Text color
                elevation=0,  # Remove shadow effect
                shape=ft.RoundedRectangleBorder(radius=20),
                text_style=ft.TextStyle(size=13)
            )
        )

        # Main Layout with Profile Container at the Top
        self.controls = [
            ft.Container(
                expand=True,
                bgcolor=self.bg,
                content=ft.Column(
                    expand=True,
                    controls=[
                        self.profile_container,  # Add Profile Container to the topd
                        self.name_container,
                        ft.Divider(height=25, color="transparent"), 
                        ft.Container(
                            padding=ft.padding.only(left=20, right=20, top=0, bottom=30),
                            alignment=ft.alignment.center,  # Centering the buttons horizontally
                            content=ft.Row(
                                controls=[
                                    self.skip_button,
                                    self.proceed_button
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Ensures horizontal centering
                            )
                        ) # Button sticks to the bottom
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Pushes button to the bottom
                )
            )
        ]

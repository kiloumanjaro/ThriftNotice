import flet as ft
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Profile(ft.View):
    def __init__(self, page: ft.Page): 
        super(Profile, self).__init__(
            route="/profile", horizontal_alignment="center",
            vertical_alignment="center", padding=0,
        )
        self.page = page
        self.wg = '#f8f9ff'
        self.bg = '#1c1c1c'
        self.bg1 = '#323232'
        self.fg='#98e2f6'
        self.bgcolor = self.bg
        self.users_api_url = os.getenv("USERS_PREF_API_URL") 

        # Profile Icon
        self.profile_icon = ft.Container(
            content=ft.Icon(name=ft.icons.FACE, size=200, color="#1c1c1c"),
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

        self.name_input = ft.TextField(
                            label="Who are you?",
                            border="none",  # Remove default border
                            bgcolor=self.bg1,  # Match container background
                            color="white",  # Text color
                            label_style=ft.TextStyle(color="white"),  # Make label white
                        )

        self.name_container = ft.Container(
            padding=ft.padding.only(left=40, right=40, top=0, bottom=0),
            content=ft.Column(
                controls=[ 
                    ft.Container(
                        bgcolor=self.bg1,  # Match background
                        border_radius=10,  # Rounded corners
                        padding=ft.padding.all(5),  # Add padding to prevent clipping
                        content= self.name_input,
                    ),
                    ft.Divider(height=30, color="transparent"),
                    ft.Container(
                        padding=ft.padding.only(left=30, right=30),
                        content=ft.Text("Would you like AI to assist you?", size=28, text_align="center", color="White")
                    )
                        
                ]    
            )
        )

        def submit_button(choice, e):
            response = requests.get(f"{self.users_api_url}get_user/?username={self.name_input.value}")
            if response.status_code == 200:
                response_data = response.json()
                username = response_data["username"]

                if self.name_input.value == username:
                    self.name_input.value = None
                    self.page.update()
            else:
                self.page.session.set("username", self.name_input.value)
                if choice == 1:
                    self.page.go("/questions") 
                else:
                    try:
                        data = {"username": self.name_input.value}
                        
                        response = requests.post(self.users_api_url, json=data)
                        response = requests.get(f"{self.users_api_url}get_user/?username={self.name_input.value}")
                        
                        if response.status_code == 200: 
                            new_user = response.json()  
                            user_id = new_user["userid"]
                            self.page.session.set("userid", user_id)
                            print("Users Pref Added!")
                            self.page.snack_bar = ft.SnackBar(ft.Text("Users pref added successfully!"), bgcolor="green")
                        else:
                            print("Error:", response.json())
                            self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add users pref"), bgcolor="red")

                    except Exception as ex:
                        print("Request failed:", ex)
                        self.page.snack_bar = ft.SnackBar(ft.Text(f"Request failed: {ex}"), bgcolor="red")

                    self.page.go("/maps")

        self.proceed_button = ft.ElevatedButton(
            text="Proceed",
            on_click=lambda e: submit_button(1, e),
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
            on_click=lambda e: submit_button(0, e),
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

import flet as ft
import requests
from dotenv import load_dotenv
import os
import json # Import json module for JSONDecodeError

load_dotenv()

class Log_in(ft.View):
    def __init__(self, page: ft.Page):
        super(Log_in, self).__init__(
            route="/log_in", horizontal_alignment="center",
            vertical_alignment="center", padding=0,
        )
        self.page = page
        self.wg = '#f8f9ff'
        self.bg = '#1c1c1c'
        self.bg1 = '#323232'
        self.fg='#98e2f6'
        self.bgcolor = self.bg
        self.users_api_url = os.getenv("USERS_PREF_API_URL")

        if not self.users_api_url: # Environment variable check in __init__
            print("Error: USERS_PREF_API_URL environment variable is not set in Log_in class.") # Debug: missing env var

        self.profile_icon = ft.Container(
            content=ft.Icon(name=ft.icons.LOCK_PERSON, size=200, color="#1c1c1c"),
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
                        content=ft.Text("Your notice to start thrifting!", size=28, text_align="center", color="White")
                    )

                ]
            )
        )

        def submit_button(choice, e): # Modified submit_button for robust error handling
            if choice == 0: # Login path
                username = self.name_input.value
                if not username: # Basic input validation
                    self.name_input.hint_text = "Please enter a username"
                    self.page.update()
                    return

                try:
                    print(f"Logging in user: {username}...") # Debug: Log login attempt
                    # Corrected URL path to /api/users/user/
                    response = requests.get(f"{self.users_api_url}user/?username={username}")
                    response.raise_for_status() # Raise HTTPError for bad responses
                    response_data = response.json()
                    print(f"API Response Data: {response_data}") # Debug: Log API response

                    # Access nested data correctly: response_data['data']
                    user_data = response_data.get('data', {}) # Use .get() with default empty dict for safety
                    retrieved_username = user_data.get("username") # Use .get() for safety
                    user_id = user_data.get("userid") # Use .get() for safety


                    if not isinstance(response_data, dict) or not isinstance(user_data, dict) or retrieved_username is None or user_id is None: # Data validation - check nested data
                        print("Warning: Invalid API response format or missing keys.") # Debug: Data validation warning
                        self.name_input.hint_text = "Login failed, please try again" # User feedback for data issue
                        self.name_input.value = None
                        self.page.update()
                        return

                    if username == retrieved_username: # Client-side username check
                        self.page.session.set("userid", user_id)
                        self.page.session.set("username", username)
                        self.page.go("/maps")
                        self.page.update()
                    else:
                        print("Warning: Incorrect username from API response.") # Debug: Username mismatch
                        self.name_input.hint_text = "INCORRECT USERNAME"
                        self.name_input.value = None
                        self.page.update()

                except requests.exceptions.RequestException as e:
                    print(f"Request exception during login: {e}") # Debug: Request exception
                    self.name_input.hint_text = "Login service unavailable" # User feedback for network issue
                    self.name_input.value = None
                    self.page.update()
                except json.JSONDecodeError as e:
                    print(f"JSON decode error during login: {e}") # Debug: JSON decode error
                    self.name_input.hint_text = "Login service error" # User feedback for JSON issue
                    self.name_input.value = None
                    self.page.update()
                except Exception as e: # Catch any other unexpected errors
                    print(f"An unexpected error occurred during login: {e}") # Debug: Unexpected error
                    self.name_input.hint_text = "Login error, try again" # User feedback for general error
                    self.name_input.value = None
                    self.page.update()
            else: # Signup path (no changes proposed for signup in this step)
                page.go("/profile")

        self.login_button = ft.ElevatedButton(
            text="Log in",
            on_click=lambda e: submit_button(0, e),
            width=190,
            height=47,
            style=ft.ButtonStyle(
                bgcolor=self.bg1,  # Background color
                color="white",  # Text color
                elevation=0,  # Remove shadow effect
                shape=ft.RoundedRectangleBorder(radius=20),
                text_style=ft.TextStyle(size=13)
            )
        )

        self.signup_button = ft.ElevatedButton(
            text="Sign up",
            on_click=lambda e: submit_button(1, e),
            width=110,
            height=47,
            style=ft.ButtonStyle(
                bgcolor=self.fg,  # Background color
                color="black",  # Text color
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
                                    self.signup_button,
                                    self.login_button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Ensures horizontal centering
                            )
                        ) # Button sticks to the bottom
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Pushes button to the bottom
                )
            )
        ]
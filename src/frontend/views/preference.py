import flet as ft
import requests
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()


class Preference(ft.View):

    def __init__(self, page: ft.Page): 
        super(Preference, self).__init__(route="/preference")
        self.page = page
        self.bg = '#1c1c1c'
        self.bg1 = '#323232'
        self.initialize()
    
    def initialize(self):
        self.controls = [self.display_questionaire_container()]
    
    def go_back_to_maps(self, e):
        self.page.go("/maps")
        #self.page.update()

    
    def display_questionaire_container(self):
        
        self.clothing_dropdown = ft.Dropdown(
            border_color="transparent",
            hint_text="Select your clothing style",
            width=291,
            text_style=ft.TextStyle(size=11, color="gray"),
            options=[
                ft.dropdown.Option("Casual wear"),
                ft.dropdown.Option("Vintage pieces"),
                ft.dropdown.Option("Formal attire"),
                ft.dropdown.Option("Streetwear"),
                ft.dropdown.Option("Designer/Branded items"),
            ]
        )
        
        self.budget_dropdown = ft.Dropdown(
            border_color="transparent",
            hint_text="What is your preferred price range per item?",
            width=291,
            hint_style=ft.TextStyle(size=11, color="black"),
            options=[
                ft.dropdown.Option("Below 50"),
                ft.dropdown.Option("50-150"),
                ft.dropdown.Option("150-300"),
                ft.dropdown.Option("300-500"),
                ft.dropdown.Option("500+"),
            ]
        )
        
        self.environment_dropdown = ft.Dropdown(
            border_color="transparent",
            hint_text="Do you prefer stores with air conditioning?",
            width=291,
            hint_style=ft.TextStyle(size=11, color="black"),
            options=[
                ft.dropdown.Option("Yes"),
                ft.dropdown.Option("No"),
                ft.dropdown.Option("No preference"),
            ]
        )
        
        self.organization_dropdown = ft.Dropdown(
            border_color="transparent",
            hint_text="Do you enjoy thrift stores that are:",
            width=291,
            text_style=ft.TextStyle(size=11, color="gray"),
            options=[
                ft.dropdown.Option("Open spaced and free-flowing"),
                ft.dropdown.Option("Well-organized and categorized"),
                ft.dropdown.Option("More of a “treasure hunt” style"),
                ft.dropdown.Option("No preference"),
            ]
        )
        
        self.interest_dropdown = ft.Dropdown(
            border_color="transparent",
            hint_text="Are you interested in stores that specialize in:",
            width=291,
            text_style=ft.TextStyle(size=11, color="gray"),
            options=[
                ft.dropdown.Option("Sustainable and eco-friendly fashion"),
                ft.dropdown.Option("Rare or collectors items"),
                ft.dropdown.Option("High-end secondhand fashion"),
                ft.dropdown.Option("Budget-friendly bulk buys"),
            ]
        )

        def submit_form(e):
            try:
                data = {
                    "username": self.page.session.get("username") or "Guest-101",
                    "clothing": self.clothing_dropdown.value,
                    "budget": self.budget_dropdown.value,
                    "shoppingenvironment": self.environment_dropdown.value,
                    "organization": self.organization_dropdown.value,
                    "interest": self.interest_dropdown.value
                }

                store_api_url = os.getenv("USERS_PREF_API_URL") 

                store_response = requests.post(store_api_url, json=data)

                if store_response.status_code == 201:
                    print("Users Pref Added!")
                    self.page.snack_bar = ft.SnackBar(ft.Text("Users pref added successfully!"), bgcolor="green")
                else:
                    print("Failed:", store_response.json())
                    self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add users pref"), bgcolor="red")
            
            except Exception as ex:
                print("Request failed:", ex)
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Request failed: {ex}"), bgcolor="red")

            self.page.update()

        submit_button = ft.Row(
            alignment="center",  # Center horizontally
            controls=[
                ft.ElevatedButton(
                    "Submit", 
                    on_click=submit_form,
                    width=200,  # Adjust the width as needed
                    height=50,  # Adjust the height as needed
                    style=ft.ButtonStyle(
                        bgcolor="#1c1c1c",  # Background color
                        color="white",  # Text color
                        elevation=0  # Remove shadow effect
                    )
                )
            ]
        )

        return ft.Container(
            expand=True,
            content=ft.Column(
                scroll="auto",
                expand=True,
                spacing=15,
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back_to_maps,
                                style=ft.ButtonStyle(
                                    shape={"": ft.CircleBorder()},
                                    padding=ft.padding.all(5),
                                    color="black",
                                )
                            ),
                            ft.Container(
                                padding=ft.padding.only(left=76),
                                content=ft.Text("Preferences", size=16, weight=ft.FontWeight.BOLD, color="black"),
                                alignment=ft.alignment.center
                            ),
                        ],
                        alignment="start",
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Container(
                                        content=ft.Icon(name=ft.icons.FINGERPRINT, size=200, color="#5f82a6"),
                                        bgcolor="#f8f9ff",
                                        padding=10
                                    ),
                                    alignment=ft.alignment.center,
                                    expand=True,
                                ),
                                ft.Container(
                                    padding=ft.padding.only(left=20),
                                    content=ft.Column(
                                        controls=[
                                            ft.Text("Clothing", size=14, color="black"),
                                            ft.Container(
                                                bgcolor="#eceef4",
                                                border_radius=0,
                                                border=ft.border.all(1, "black"),  # Custom border
                                                padding=ft.padding.only(bottom=2, left=6),  
                                                content=self.clothing_dropdown,
                                            ),
                                            ft.Container(height=2),
                                            ft.Text("Budget", size=14, color="black"),
                                            ft.Container(
                                                bgcolor="#eceef4",
                                                border_radius=0,
                                                border=ft.border.all(1, "black"),  # Custom border
                                                padding=ft.padding.only(bottom=2, left=6),  
                                                content=self.budget_dropdown,
                                            ),
                                            ft.Container(height=2),
                                            ft.Text("Shopping Environment", size=14, color="black"),
                                            ft.Container(
                                                bgcolor="#eceef4",
                                                border_radius=0,
                                                border=ft.border.all(1, "black"),  # Custom border
                                                padding=ft.padding.only(bottom=2, left=6),  
                                                content=self.environment_dropdown,
                                            ),
                                            ft.Container(height=2),
                                            ft.Text("Organization", size=14, color="black"),
                                            ft.Container(
                                                bgcolor="#eceef4",
                                                border_radius=0,
                                                border=ft.border.all(1, "black"),  # Custom border
                                                padding=ft.padding.only(bottom=2, left=6),  
                                                content=self.organization_dropdown,
                                            ),
                                            ft.Container(height=2),
                                            ft.Text("Interest", size=14, color="black"),
                                            ft.Container(
                                                bgcolor="#eceef4",
                                                border_radius=0,
                                                border=ft.border.all(1, "black"),  # Custom border
                                                padding=ft.padding.only(bottom=2, left=6),  
                                                content=self.interest_dropdown,
                                            ),
                                            ft.Container(height=13),
                                            submit_button
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                ]
            )
        )

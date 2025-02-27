import flet as ft
import requests
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

SUPABASE_URL = ""
GEOCODE_API_URL= ""

class Create(ft.View):

    def __init__(self, page: ft.Page): 
        super(Create, self).__init__(route="/create")
        configure()
        self.page = page
        self.initialize()

    def initialize(self):
        self.controls = [self.display_create_container()]

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()
    
    def display_create_container(self):
        self.name = ft.TextField()
        self.address = ft.TextField(multiline=True, max_lines=2)
        
        type_selector = ft.Dropdown(
            options=[
                ft.dropdown.Option("Pop-up"),
                ft.dropdown.Option("Store")
            ]
        )

        date_time_field = ft.TextField(disabled=True, width=155)

        def on_type_change(e):
            date_time_field.disabled = type_selector.value != "Pop-up"
            self.page.update()

        type_selector.on_change = on_type_change

        def submit_form(e):
            # Gather field values
            data = {
                "shopname": self.name.value,
                "formattedaddress": self.address.value,
            }

            try:
                # Geocode the address
                geocode_response = requests.post(os.getenv("GEOCODE_API_URL"), json={"address": self.address.value})

                print("Raw response status:", geocode_response.status_code)
                print("Raw response text:", geocode_response.text)  # <--- Print raw response

                if geocode_response.status_code == 200:
                    geocode_data = geocode_response.json()
                    print("Parsed JSON Response:", geocode_data)  # <--- Print parsed JSON

                    latitude = geocode_data.get("latitude")
                    longitude = geocode_data.get("longitude")

                    if latitude and longitude:
                        print(f"Coordinates: {latitude}, {longitude}")
                    else:
                        print("Latitude or longitude not found in response!")

                else:
                    print("Geocoding failed:", geocode_response.json())

            
                store_api_url = os.getenv("SUPABASE_URL")  
                supabase_api_key = os.getenv("SUPABASE_API_KEY")  

                headers = {
                    "apikey": supabase_api_key,
                    "Authorization": f"Bearer {supabase_api_key}",
                    "Content-Type": "application/json"
                }

                store_response = requests.post(store_api_url, json=data, headers=headers)

                if store_response.status_code == 201:
                    print("Store Added!")
                    self.page.snack_bar = ft.SnackBar(ft.Text("Store added successfully!"), bgcolor="green")
                else:
                    print("Failed:", store_response.json())
                    self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add store"), bgcolor="red")
            
                print("Mock store added (ignoring Supabase). Data:", data)
                self.page.snack_bar = ft.SnackBar(ft.Text("Store data processed! (Supabase skipped)"), bgcolor="blue")

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

        bg='#1c1c1c'
        fg='#98e2f6'
        wg='#f8f9ff'
        fg1='#5f82a6'

        return ft.Container(
            expand=True,
            bgcolor='white',
            content=ft.Column(
                expand=True,
                controls=[  
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back_to_maps,
                                style=ft.ButtonStyle(
                                    shape={"": ft.CircleBorder()},
                                    padding=ft.padding.all(5),
                                    bgcolor="white",
                                    color="black",
                                )
                            ),
                            ft.Container(
                                padding=ft.padding.only(left=70),
                                content=ft.Text("Add Location", size=16, weight=ft.FontWeight.BOLD),
                                alignment=ft.alignment.center
                            ),
                        ],
                        alignment="start",
                    ),
                    ft.Container(
                        padding=ft.padding.only(top=0, left=10, right=10, bottom=0),
                        alignment=ft.alignment.bottom_center,
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.MAP, color=fg1, size=180),  # Added landmark icon
                            ],
                            alignment="center"
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=20, right=20, top=0, bottom=25),
                        content=ft.Column(
                            controls=[
                                ft.Text("Title", size=13),
                                self.name,
                                ft.Text("Address", size=13),
                                self.address,
                                ft.Text("Type                                Date & Time", size=13),
                                ft.Row(  
                                    controls=[
                                        type_selector,
                                        date_time_field
                                    ],
                                    alignment="stretch"
                                ),
                                ft.Divider(height=15, color="transparent"),
                                submit_button
                            ]
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Pushes the placeholder to the bottom
            )
        )



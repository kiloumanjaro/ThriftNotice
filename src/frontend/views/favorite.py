import flet as ft
import requests
from dotenv import load_dotenv
import os
import json # Import json module for JSONDecodeError

load_dotenv()

class Favorite(ft.View):
    def __init__(self, page: ft.Page):
        super(Favorite, self).__init__(route="/favorite")
        self.bg = '#1c1c1c'
        self.fg = '#98e2f6'
        self.wg = '#f8f9ff'
        self.fg1 = '#5f82a6'
        self.bg1 = '#323232'
        self.page = page
        self.shop_container = self.create_shop_container() # Renamed to create_shop_container
        self.initialize()
        self.bgcolor = self.bg

    def initialize(self):
        self.controls = [self.display_view()] # Renamed to display_view

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def toggle_details(self, e, details_container, shop_item, shop_header, icon_button, shop_text):
        details_container.visible = not details_container.visible
        icon_button.icon = ft.icons.ARROW_DROP_DOWN if details_container.visible else ft.icons.ARROW_DROP_UP

        # Update background colors when expanded/collapsed
        icon_button.icon_color = "black" if details_container.visible else "white"
        new_bgcolor = "#98e2f6" if details_container.visible else self.bg1
        text_color = "black" if details_container.visible else "white"

        details_container.bgcolor = new_bgcolor
        shop_item.bgcolor = new_bgcolor
        shop_header.bgcolor = new_bgcolor

        # Update the shop text color
        shop_text.color = text_color

        self.page.update()


    def create_toggle_button(self, details_container, shop_item, shop_header, shop_text):
        icon_button = ft.IconButton(
            icon=ft.icons.ARROW_DROP_UP,
            icon_color="white",
            style=ft.ButtonStyle(
                bgcolor="transparent",
                overlay_color="transparent",
            ),
        )

        def toggle_details_handler(e):
            self.toggle_details(e, details_container, shop_item, shop_header, icon_button, shop_text)

        icon_button.on_click = toggle_details_handler
        return icon_button

    def fetch_favorite_shops(self): # Separated API call to fetch_favorite_shops
        favorite_shop_url = os.getenv("FAVORITE_API_URL")
        if not favorite_shop_url:
            print("Error: FAVORITE_API_URL environment variable is not set for fetching favorites.") # Debug: missing env var
            return None

        try:
            print(f"Fetching favorite shops for user ID: {self.page.session.get("userid")}...") # Debug: log fetch attempt
            # Corrected URL path to /api/favoriteshop/favorite-shops/
            favorite_response = requests.get(f"{favorite_shop_url}favorite-shops/?userid={self.page.session.get("userid")}")
            favorite_response.raise_for_status() # Raise HTTPError for bad responses
            response_data = favorite_response.json() # Capture json data
            print(f"API Response Data: {response_data}") # Debug: API response

            if not isinstance(response_data, dict) or 'data' not in response_data or not isinstance(response_data['data'], list):
                print("Warning: Invalid API response format or missing 'data' key.") # Debug: data validation warning
                return None

            return response_data['data'] # Return the list of favorite shops

        except requests.exceptions.RequestException as e:
            print(f"Request exception during favorite shops fetch: {e}") # Debug: request exception
            return None
        except json.JSONDecodeError as e: # Handle JSONDecodeError
            print(f"JSON decode error during favorite shops fetch: {e}") # Debug: JSON decode error
            return None
        except Exception as e: # Catch any other exceptions
            print(f"An unexpected error occurred during favorite shops fetch: {e}") # Debug: unexpected error
            return None

    def create_shop_item_ui(self, favorite_shop, index): # Encapsulated UI creation for shop item
        shop_address = favorite_shop.get("formattedaddress", "N/A") # Use .get() with default
        shop_name = favorite_shop.get("shopname", f"Shop {index + 1}") # Use .get() with default

        details_container = ft.Container(
            visible=False,
            content=ft.Column(
                controls=[
                    ft.Text(shop_address, size=12, color="black", italic=True),
                ],
            ),
            padding=ft.padding.only(left=15, right=20, top=0, bottom=15),
            bgcolor=self.bg1,
            border_radius=5
        )

        shop_item = ft.Container(
            bgcolor=self.bg1,
            border_radius=10,
            padding=ft.padding.symmetric(vertical=3, horizontal=10),
            margin=ft.margin.symmetric(vertical=3, horizontal=15),
        )

        shop_header = ft.Container(
            height=40,
            bgcolor=self.bg1,
            border_radius=8,
            padding=ft.padding.only(left=15, right=3, top=3, bottom=3),
        )

        # Shop title text (so we can modify its color dynamically)
        shop_text = ft.Text(f"{index+1}. {shop_name}", size=13, color="white")

        # Create toggle button with updated reference
        icon_button = self.create_toggle_button(details_container, shop_item, shop_header, shop_text)

        shop_header.content = ft.Row(
            controls=[
                shop_text, # Forces text to the left
                ft.Container(
                    content=icon_button,
                    alignment=ft.alignment.center_right, # Ensures button is fully to the right
                ),
            ],
            alignment="spaceBetween",
        )

        shop_item.content = ft.Column(
            controls=[
                shop_header,
                details_container,
            ],
            spacing=0,
        )
        return shop_item

    def create_shop_container(self): # Renamed and refactored create_shop to create_shop_container
        container = ft.Container(
            expand=True,
            padding=ft.padding.symmetric(horizontal=0),
            content=ft.Column(expand=True, scroll="always", controls=[]),  # Ensure scrollbar is always visible
        )

        favorite_data = self.fetch_favorite_shops() # Fetch favorite shops using the new method

        if favorite_data and isinstance(favorite_data, list): # Check if data is valid and is a list
            print("Favorite shops data fetched successfully!") # Debug: success message
            if not favorite_data: # Check if favorite_data list is empty
                container.content.controls.extend([self.create_placeholder_item_ui(i) for i in range(4)]) # Display placeholders if no favorites
            else:
                for i, favorite_shop in enumerate(favorite_data): # Iterate through valid data
                    if isinstance(favorite_shop, dict): # Validate each item is a dict
                        shop_item = self.create_shop_item_ui(favorite_shop, i) # Create shop item UI
                        container.content.controls.append(shop_item) # Append to container
                    else:
                        print(f"Warning: favorite_shop item is not a dictionary: {favorite_shop}") # Debug: non-dict shop_item
        else:
            print("Warning: No favorite shops data fetched or invalid data format.") # Debug: no data or invalid format
            container.content.controls.extend([self.create_placeholder_item_ui(i) for i in range(4)]) # Display placeholders if fetch fails or data is invalid

        return container

    def create_placeholder_item_ui(self, index): # Encapsulated placeholder UI creation
        details_container = ft.Container(
            visible=False,
            content=ft.Column(
                controls=[
                    ft.Text("Add a favorite shop first!", size=12, color="black", italic=True),
                ],
            ),
            padding=ft.padding.only(left=15, right=20, top=0, bottom=15),
            bgcolor=self.bg1,
            border_radius=5
        )

        shop_item = ft.Container(
            bgcolor=self.bg1,
            border_radius=10,
            padding=ft.padding.symmetric(vertical=3, horizontal=10),
            margin=ft.margin.symmetric(vertical=3, horizontal=15),
        )

        shop_header = ft.Container(
            height=40,
            bgcolor=self.bg1,
            border_radius=8,
            padding=ft.padding.only(left=15, right=3, top=3, bottom=3),
        )

        # Shop title text (so we can modify its color dynamically)
        shop_text = ft.Text(f"Shop {index+1}", size=13, color="white")

        # Create toggle button with updated reference
        icon_button = self.create_toggle_button(details_container, shop_item, shop_header, shop_text)

        shop_header.content = ft.Row(
            controls=[
                shop_text, # Forces text to the left
                ft.Container(
                    content=icon_button,
                    alignment=ft.alignment.center_right, # Ensures button is fully to the right
                ),
            ],
            alignment="spaceBetween",
        )

        shop_item.content = ft.Column(
            controls=[
                shop_header,
                details_container,
            ],
            spacing=0,
        )
        return shop_item


    def display_view(self): # Renamed display_shop_container to display_view
        return ft.Column(
            height=700,
            scroll="auto",  # Allow scrolling for this section
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=self.go_back_to_maps,
                            style=ft.ButtonStyle(
                                shape={"": ft.CircleBorder()},
                                padding=ft.padding.all(5),
                                bgcolor=self.bg,
                                color="white",
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.only(left=83),
                            content=ft.Text("Favorites", size=16, weight=ft.FontWeight.BOLD, color='white'),
                            alignment=ft.alignment.center
                        ),
                    ],
                    alignment="start",
                ),
                ft.Container(
                    alignment=ft.alignment.center,  # Centers the icon
                    padding=ft.padding.only(top=12, bottom=28),  # Adds spacing
                    content=ft.Icon(ft.icons.STORE, color="white", size=180)  # Large favorite icon
                ),
                ft.Container(
                    height=323,
                    content=ft.Stack(
                        expand=True,
                        controls=[
                            self.shop_container,
                            # Floating Action Button
                            ft.FloatingActionButton(

                                bottom=2, right=20,
                                icon=ft.icons.ADD,
                                on_click=lambda e: self.page.go("/maps"),
                                bgcolor="white",
                                foreground_color=self.bg,
                                shape=ft.CircleBorder()
                            )
                        ]
                    ),
                )
            ]
        )
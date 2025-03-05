import flet as ft
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Shop(ft.View):
    def __init__(self, page: ft.Page, shop_id):
        super(Shop, self).__init__(route="/shop", padding=0, bgcolor='white')
        self.page = page
        self.shop_id = shop_id[0]
        self.shop_name = None
        self.formatted_address = None
        self.short_description = None
        self.reviews = [f"Great shop {self.shop_id}!", "Nice collection!", "Affordable and unique items."] # Reviews are still placeholders as per instruction
        self.is_favorite = False

        self.initialize()

    def initialize(self):
        self.fetch_reviews()
        self.fetch_shop_data(self.shop_id)
        self.controls = [self.display_shop_container()]

    def fetch_shop_data(self, shop_id):
        api_url = os.getenv("THRIFTSTORE_API_URL")  # Base API URL for thriftstore data
        if not api_url:
            print("THRIFTSTORE_API_URL environment variable is not set.")
            return None

        api_endpoint = f"{api_url}"  # Use base URL to fetch all stores

        try:
            response_one = requests.get(api_endpoint)
            if response_one.status_code == 200:
                all_shops_data = response_one.json()  # Get list of all shops

                for shop_data in all_shops_data:  # Loop through all shops in the API response
                    if int(shop_data.get('shopid')) == int(self.shop_id):  # Compare with integer shop_id
                        self.shop_name = shop_data.get('shopname')
                        self.formatted_address = shop_data.get('formattedaddress')
                        self.short_description = shop_data.get('shortdescription')
                        return shop_data  # Return the shop data if shop_id matches

                print(f"Shop ID {shop_id} (integer: {self.shop_id}) not found in API response.") # Use both original and integer shop_id in print
                return None # Shop ID not found

            else:
                print(f"Error fetching shop data: {response_one.status_code} - {response_one.text}")
                return None
        except ValueError: # Handle case where shop_id_value cannot be converted to integer
            print(f"Error: Shop ID '{self.shop_id}' is not a valid integer.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            return None
        
    def fetch_reviews(self):
        review_api_url = os.getenv("USERS_REVIEW_API_URL")
        response = requests.get(f"{review_api_url}get_reviews/?shopid={self.shop_id}")

        if response.status_code == 200:
            all_reviews = response.json()
            print(all_reviews)
            new_reviews = [review["review"] for review in all_reviews]
            self.reviews = new_reviews
        else:
            print("Could not find any reviews")
        
    def toggle_favorite(self, e):
        self.is_favorite = not self.is_favorite

        print("--- toggle_favorite START ---") # Debug: Function entry
        print(f"Shop ID: {self.shop_id}") # Debug: Shop ID
        print(f"Current is_favorite: {self.is_favorite}") # Debug: Favorite state
        print(f"Page Session (before get userid): {self.page.session}") # Debug: Full session *before* userid retrieval

        userid = self.page.session.get("userid")

        print(f"User ID from session: {userid}") # Debug: Retrieved userid

        if not userid:
            print("blrgheee: User ID not found in session. Cannot toggle favorite.") # Original error message
            print("--- toggle_favorite END (userid missing) ---") # Debug: Function exit - missing userid
            return

        favorite_url = os.getenv("FAVORITE_API_URL")
        if not favorite_url:
            print("Error: FAVORITE_API_URL environment variable is not set for toggle_favorite.") # Debug: missing env var
            print("--- toggle_favorite END (missing API URL) ---") # Debug: Function exit - missing API URL
            return

        data = {
            "userid": userid, # Use the retrieved userid
            "shopid": self.shop_id,
        }

        try: # Wrap API call in try-except for robustness
            if self.is_favorite:
                print("Adding to favorites...") # Debug: Adding favorite
                response = requests.post(favorite_url, json=data)
            else:
                print("Removing from favorites...") # Debug: Removing favorite
                response = requests.delete(f"{favorite_url}delete_favorite_shop/?userid={userid}&shopid={self.shop_id}") # Use retrieved userid

            response.raise_for_status() # Raise HTTPError for bad responses

            if response.status_code == 201 or response.status_code == 200: # Handle both 201 (POST) and 200 (DELETE) success
                action_message = "added" if self.is_favorite else "removed"
                print(f"Favorite shop {action_message} successfully! Status Code: {response.status_code}") # Debug: API success
            else:
                print(f"Warning: Favorite shop action failed. Status Code: {response.status_code}, Response: {response.text}") # Debug: API failure - status code
        except requests.exceptions.RequestException as e:
            print(f"Request exception during favorite toggle: {e}") # Debug: Request exception
        except json.JSONDecodeError as e: # Handle JSONDecodeError
            print(f"JSON decode error during favorite toggle: {e}") # Debug: JSON decode error
        except Exception as e: # Catch any other exceptions
            print(f"An unexpected error occurred during favorite toggle: {e}") # Debug: Unexpected error
        finally:
            print("--- toggle_favorite END ---") # Debug: Function exit (normal or error)


        self.favorite_button.icon = ft.icons.FAVORITE_BORDER if not self.is_favorite else ft.icons.FAVORITE
        self.favorite_button.icon_color = "#323232" if not self.is_favorite else "red"
        self.favorite_button.update()
        self.page.update()

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def display_shop_container(self):
        self.favorite_button = ft.IconButton(
            icon=ft.icons.FAVORITE_BORDER,
            icon_size=20,
            icon_color="#323232",
            on_click=self.toggle_favorite,
        )

        self.review_items = [ # Reviews are still placeholders as per instruction
            ft.Container(
                bgcolor="#f8f9ff",
                padding=8,
                border_radius=10,
                border=ft.border.all(0.5, "black"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30),
                        ft.Text(review, size=12, color="black"),
                    ],
                    spacing=10,
                )
            )
            for review in self.reviews
        ]

        return ft.Container(
            expand=True,
            padding=ft.padding.only(bottom=10),
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        top=0,
                        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
                        content=ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Image(
                                src="placeholder.png", # Still placeholder image
                                width=380,
                                height=280,
                                fit=ft.ImageFit.COVER,
                            ),
                        ),
                    ),
                    ft.Container(
                        top=220,
                        width=360,
                        height=500,
                        bgcolor="white",
                        padding=ft.padding.only(left=25, right=25, top=20),
                        border_radius=ft.border_radius.only(top_left=20, top_right=20),
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(self.shop_name or 'N/A', size=23, weight="bold", color="black"), # Use fetched shop_name or 'N/A'
                                ft.Text(self.formatted_address or 'N/A', size=10, color="black"), # Use fetched formatted_address or 'N/A'
                                ft.Divider(height=5, color="transparent"),
                                ft.Text("Community Reviews", size=10, color="black"),
                                ft.Container(
                                    expand=True,
                                    padding=ft.padding.only(top=5),
                                    content=ft.Column(controls=self.review_items)
                                )
                            ]
                        ),
                    ),
                    # Favorite icon inside a circular background
                    ft.Container(
                        top=197,
                        right=35,
                        width=45,
                        height=45,
                        bgcolor="white",
                        border_radius=50,
                        border=ft.border.all(0.5, "#1c1c1c"),
                        alignment=ft.alignment.center,
                        content=self.favorite_button
                    ),
                    # Floating button for maps
                    ft.Container(
                        bottom=10,
                        right=35,
                        width=50,
                        height=50,
                        bgcolor="#1c1c1c",
                        border_radius=50,
                        alignment=ft.alignment.center,
                        content=ft.IconButton(
                            icon=ft.icons.HOME,
                            icon_size=20,
                            icon_color="white",
                            on_click=self.go_back_to_maps
                        )
                    ),
                ]
            ),
        )
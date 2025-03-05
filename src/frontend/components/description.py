import flet as ft
import requests
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

class BottomSheet(ft.Container):
    def __init__(self, on_close):
        self.configure()
        self.client = self.create_client()

        super().__init__(
            width=322,
            height=350,
            bgcolor="white",
            border_radius=ft.border_radius.all(20),
            margin=ft.margin.only(bottom=23, left=20),
            padding=ft.padding.only(top=20, bottom=20, right=15, left=25),
            bottom=-400,
            animate_position=ft.animation.Animation(400, "decelerate"),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=3,
                color=ft.colors.BLACK12,
                offset=ft.Offset(0, 1)
            )
        )

        self.initialize(on_close)

    def configure(self):
        load_dotenv()

    def create_client(self):
        return genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

    def initialize(self, on_close):
        self.current_shop_id = None
        self.shop_name_placeholder = 'Shop Name' # Placeholder, will be updated dynamically
        self.formatted_address_placeholder = 'Address' # Placeholder, will be updated dynamically
        self.short_description_placeholder = "Description" # Placeholder, will be updated dynamically
        self.review_text = ft.TextField(hint_text="Write a review...", text_style=ft.TextStyle(size=12, color="gray"), border_radius=10, height=40)

        self.shop_name_text = ft.TextButton(
                                            self.shop_name_placeholder,
                                            on_click=lambda e: self.page.go(f"/shop?shop_id={self.current_shop_id}"), # Modified lambda
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(size=23, weight="bold",),
                                                padding=0,
                                        )
                                    )
        self.address_text = ft.Text(self.formatted_address_placeholder, size=10) # Use placeholder initially
        self.description_text = ft.Text(self.short_description_placeholder, size=12) # Use placeholder initially


        self.content = ft.Column(
            expand=True,
            spacing=5,
            controls=[
                ft.Row(
                    alignment='spaceBetween',
                    controls=[
                        self.shop_name_text, # Use TextButton widget
                        ft.IconButton(ft.icons.CLOSE, on_click=on_close, icon_size=20),
                    ]
                ),
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(right=15),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            self.address_text, # Use Text widget
                            self.description_text, # Use Text widget
                        ]
                    )
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Row(
                    controls=[
                        ft.Container(
                            width=220,
                            content=self.review_text
                        ),
                        ft.IconButton(
                            icon=ft.icons.SEND,
                            icon_size=20,
                            tooltip="Submit Review",
                            on_click=self.submit_form
                        )
                    ]
                )
            ]
        )

    def submit_form(self, e):
        try:
            store_api_url = os.getenv("THRIFTSTORE_API_URL")
            data = {
                "shopname": self.shop_name_text.text, # Use the updated shop name from TextButton
                "review": self.review_text.value,
            }
            store_response = requests.post(store_api_url, json=data)

            if store_response.status_code == 201:
                print("\nReview Added!")
                self.page.snack_bar = ft.SnackBar(ft.Text("Review added successfully!"), bgcolor="green")
                self.summarize_and_update()
            else:
                print("Failed:", store_response.json())
                self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add review"), bgcolor="red")
        except Exception as ex:
            print("Request failed:", ex)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Request failed: {ex}"), bgcolor="red")
    
        try:
            review_api_url = os.getenv("USERS_REVIEW_API_URL")
            data = {
                "shopid": self.current_shop_id,
                "review": self.review_text.value,
            }
            response = requests.post(review_api_url, json=data)

            if response.status_code == 201:
                print("\nReview Added to Review Table!")
                self.page.snack_bar = ft.SnackBar(ft.Text("Review added successfully!"), bgcolor="green")
                self.summarize_and_update()
            else:
                print("Failed to add to review table:", store_response.json())
                self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add review"), bgcolor="red")
        except Exception as ex:
            print("Request failed to review table:", ex)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Request failed to review table: {ex}"), bgcolor="red")

    def summarize_reviews(self, text1: str, text2: str, max_length: int = 425) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Summarize these reviews into one concise and engaging review (max {max_length} chars):\n\n"
                      f"Review 1: {text1}\n\nReview 2: {text2}"],
            config=types.GenerateContentConfig(
                max_output_tokens=500,
                temperature=0.1
            )
        )
        return response.text.strip() if response and response.text else "Error: No response generated."

    def summarize_and_update(self):
        new_review = self.review_text.value.strip()
        if not new_review:
            return

        summarized_text = self.summarize_reviews(self.description_text.value, new_review) # Use the updated description text
        print(summarized_text)
        self.description_text.value = summarized_text # Update the Text widget's value
        self.description_text.update() # Update the Text widget on the page
        self.page.update()

    def show(self, marker_data):
            if marker_data:
                self.current_shop_id = marker_data.get('shopid') # Store shop ID
                self.shop_name_text.text = marker_data.get('shopname', self.shop_name_placeholder)
                self.address_text.value = marker_data.get('formattedaddress', self.formatted_address_placeholder)
                self.description_text.value = marker_data.get('shortdescription', self.short_description_placeholder)

                self.shop_name_text.update()
                self.address_text.update()
                self.description_text.update()

            self.bottom = 0
            self.update()

    def hide(self):
        self.bottom = -400
        self.update()
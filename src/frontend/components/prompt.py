import flet as ft
import requests
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import re

class Prompt(ft.Container):
    def __init__(self, on_close):
        self.configure()
        self.client = self.create_client()
        self.description_text = ft.Text("Description", size=11, color="#36618e")

        super().__init__(
            width=322,
            height=280,
            bgcolor=ft.colors.with_opacity(0.8, "#ececec"),
            border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15, bottom_right=15),
            border=ft.border.all(0.5, "#b6b6b6"),
            margin=ft.margin.only(bottom=23, left=20),
            padding=0,
            top=-400,
            animate_position=ft.animation.Animation(400, "decelerate"),
        )

        self.initialize(on_close)

    def configure(self):
        load_dotenv()

    def create_client(self):
        return genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

    def initialize(self, on_close):
        
        self.shop_name_text = ft.TextButton(
                "Shop Name",
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(size=20, weight="bold",),
                    padding=0,
            )
        )

        self.address_text = ft.Text("Address", size=10)
        

        self.content = ft.Container(
            margin=ft.margin.only(right=3, left=3, top=3, bottom=3),
            padding=ft.padding.only(left=20, top=5, bottom=15, right=10),
            border_radius=ft.border_radius.only(top_left=10, top_right=10, bottom_left=10, bottom_right=10),
            bgcolor="white",
            border=ft.border.all(1, "#c9c9c9"),
            content=ft.Column(
            expand=True,
            spacing=5,
            controls=[
                ft.Row(
                    alignment='spaceBetween',
                    controls=[
                        self.shop_name_text,
                        ft.IconButton(ft.icons.CLOSE, on_click=on_close, icon_size=20),
                    ]
                ),
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(right=15),
                    content=ft.Column(
                        spacing=15,
                        controls=[
                            self.description_text,
                        ]
                    )
                ),
            ]
        )
    )

    def submit_form(self, e):
        try:
            store_api_url = os.getenv("THRIFTSTORE_API_URL")
            data = {
                "shopname": self.shop_name_text.text,
            }
            store_response = requests.post(store_api_url, json=data)

            if store_response.status_code == 201:
                print("Review Added!")
                self.page.snack_bar = ft.SnackBar(ft.Text("Review added successfully!"), bgcolor="green")
                self.summarize_and_update()
            else:
                print("Failed:", store_response.json())
                self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add review"), bgcolor="red")
        except Exception as ex:
            print("Request failed:", ex)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Request failed: {ex}"), bgcolor="red")
        self.page.update()

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

    def show(self):
        self.top = 15
        self.update()

    def hide(self):
        self.top = -400
        self.update()

    def extract_shop_id(self, text):
        match = re.search(r'\[(\d+)\]', text)  # Use 'text' instead of 'self.text'
        if match:
            return int(match.group(1))  # Convert matched ID to integer
        return None  # Return None if no match is found

    def update_prompt(self, message):
        """Update the displayed text in the Prompt."""
        self.description_text.value = message
        shop_id = self.extract_shop_id(self.description_text.value)  # Fix: added 'self.'
        self.update()

    


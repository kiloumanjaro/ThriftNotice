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
            width=318,
            height=360,
            bgcolor="white",
            border_radius=ft.border_radius.all(20),
            margin=ft.margin.only(bottom=23),
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
        self.shop_name = 'Shop Name'
        self.formatted_address = '123 Vintage Lane, Suite 5, Brookville, USA'
        self.short_description = "Nestled in the heart of the city, Timeless Treasures Thrift Shop is a hidden gem for bargain hunters and vintage lovers alike. Our shop offers a carefully curated selection of pre-loved clothing, unique home décor, rare collectibles, and secondhand books—all at unbeatable prices. Whether you're searching for a one-of-a-kind fashion statement, a nostalgic keepsake, or simply a great deal, our ever-changing inventory has something for everyone."
        self.review_text = ft.TextField(hint_text="Write a review...", text_style=ft.TextStyle(size=12, color="gray"), border_radius=10, height=40)
        
        self.content = ft.Column(
            expand=True,
            spacing=5,
            controls=[
                ft.Row(
                    alignment='spaceBetween',
                    controls=[
                        ft.Text(self.shop_name, size=23, weight='bold'),
                        ft.IconButton(ft.icons.CLOSE, on_click=on_close, icon_size=20),
                    ]
                ),
                ft.Container(
                    expand=True,
                    padding=ft.padding.only(right=15),
                    content=ft.Column(
                        controls=[
                            ft.Text(self.formatted_address, size=10),
                            ft.Text(self.short_description, size=12),
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
                "shopname": self.shop_name,
                "review": self.review_text.value,
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
    
    def summarize_and_update(self):
        new_review = self.review_text.value.strip()
        if not new_review:
            return
        
        summarized_text = self.summarize_reviews(self.short_description, new_review)
        print(summarized_text)
        self.content.controls[1].content.controls[1].value = summarized_text
        self.content.controls[1].content.controls[1].update()
        self.page.update()
    
    def show(self):
        self.bottom = 0
        self.update()
    
    def hide(self):
        self.bottom = -400
        self.update()

import flet as ft
from .clothing import clothing_page
from .budget import budget_page
from .shopping_environment import shopping_environment_page
from .organization import organization_page
from .interest import interest_page
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Questions(ft.View):
    def __init__(self, page: ft.Page): 
        super(Questions, self).__init__(route="/questions")
        self.page = page
        self.current_page = 0  
        self.username = self.page.session.get("username")
        # Stores user selections for different categories
        self.user_preferences = {
            "username": self.username,
            "clothing": None,
            "budget": None,
            "shoppingenvironment": None,
            "organization": None,
            "interest": None
        }

        # Initialize pages while passing self for navigation and user preference tracking
        self.pages = [
            clothing_page(self),
            budget_page(self),
            shopping_environment_page(self),
            organization_page(self),
            interest_page(self)
        ]


        self.initialize()

    def initialize(self):
        self.show_current_page()

    def show_current_page(self):
        """Update UI with the current question page and buttons."""
        self.controls = [
            self.pages[self.current_page],
        ]
        # Disable the next button if no option is selected for the current category
        self.page.update()

    def next_page(self, e):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_current_page()

    def prev_page(self, e):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()

    def set_page(self, index):
        """Set the current page to a specific index and update the UI."""
        if 0 <= index < len(self.pages):
            self.current_page = index
            self.show_current_page()

    def go_back_to_maps(self, e):
        print("User Preferences:", self.user_preferences) 

        try:
                data = self.user_preferences
                users_api_url = os.getenv("USERS_PREF_API_URL") 

                users_response = requests.post(users_api_url, json=data)
                users_response = requests.get(f"{users_api_url}get_user/?username={self.username}")

                if users_response.status_code == 200:
                    new_user = users_response.json()  
                    user_id = new_user["userid"]
                    self.page.session.set("userid", user_id)
                    print("Users Preference Added!\n")
                    self.page.snack_bar = ft.SnackBar(ft.Text("Users pref added successfully!"), bgcolor="green")
                else:
                    print("Failed:", users_response.json())
                    self.page.snack_bar = ft.SnackBar(ft.Text("Failed to add users pref"), bgcolor="red")
            
        except Exception as ex:
            print("Request failed:", ex)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Request failed: {ex}"), bgcolor="red")

        self.page.go("/maps")

    def update_preference(self, category, value):
        """Updates the selected user preference and enables Next if a choice is made."""
        self.user_preferences[category] = value
        self.show_current_page()  # Ensure UI updates after changing preference

    def get_current_category(self):
        """Returns the category associated with the current page index."""
        categories = list(self.user_preferences.keys())
        return categories[self.current_page]

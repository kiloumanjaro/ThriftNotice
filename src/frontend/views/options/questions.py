import flet as ft
from .clothing import clothing_page
from .budget import budget_page
from .shopping_environment import shopping_environment_page
from .organization import organization_page
from .interest import interest_page

class Questions(ft.View):
    def __init__(self, page: ft.Page): 
        super(Questions, self).__init__(route="/questions")
        self.page = page
        self.current_page = 0  

        # Stores user selections for different categories
        self.user_preferences = {
            "clothing": None,
            "budget": None,
            "shopping_environment": None,
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

        # Next button (initially disabled)
        self.next_button = ft.ElevatedButton("Next", on_click=self.next_page, disabled=True)

        self.initialize()

    def initialize(self):
        self.show_current_page()

    def show_current_page(self):
        """Update UI with the current question page and buttons."""
        self.controls = [
            self.pages[self.current_page],
            self.next_button  # Include the next button in the UI
        ]
        # Disable the next button if no option is selected for the current category
        self.next_button.disabled = self.user_preferences[self.get_current_category()] is None
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
        self.page.go("/maps")
        self.page.update()

    def update_preference(self, category, value):
        """Updates the selected user preference and enables Next if a choice is made."""
        self.user_preferences[category] = value
        if category == self.get_current_category():
            self.next_button.disabled = False
        self.show_current_page()  # Ensure UI updates after changing preference

    def get_current_category(self):
        """Returns the category associated with the current page index."""
        categories = list(self.user_preferences.keys())
        return categories[self.current_page]

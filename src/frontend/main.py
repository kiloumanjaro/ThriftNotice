import flet as ft
from dotenv import load_dotenv
import os

# Load environment variables at the start
def configure():
    load_dotenv()

configure()  # Call it once at the beginning of the script

from views.landing import Landing
from views.maps import Maps
from views.favorite import Favorite
from views.options.questions import Questions
from views.create import Create
from views.preference import Preference
from views.about import About
from views.profile import Profile
from views.shop import Shop  # Import the Shop view
from views.ai import AI
from views.log_in import Log_in

if os.name == "nt":  # Windows
    os.system("cls")
else:  # macOS and Linux
    os.system("clear")

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667
    page.window.resizable = False
    page.update()

    def router(route):
        page.views.clear()
        current_route = page.route

        if current_route == "/":
            page.views.append(Landing(page))

        elif current_route == "/maps":
            maps = Maps(page)
            maps.padding = 0
            page.views.append(maps)

        elif current_route == "/favorite":
            page.views.append(Favorite(page))

        elif current_route == "/create":
            page.views.append(Create(page))  # Create usess API_URL

        elif current_route == "/questions":
            page.views.append(Questions(page))

        elif current_route == "/preference":
            page.views.append(Preference(page))

        elif current_route == "/about":
            about = About(page)
            about.padding = 0
            page.views.append(about)

        elif current_route.startswith("/shop"): # Catch /shop and its parameters
            uri = Uri.parse(current_route) # Parse the route
            shop_id = uri.query_params.get("shop_id") # Extract shop_id
            if shop_id:
                shop = Shop(page, shop_id=shop_id) # Pass shop_id to Shop view
                shop.padding = 0
                page.views.append(shop)
            else:
                # Handle case where shop_id is missing in the route, maybe go to an error page or maps
                page.views.append(Maps(page)) # Or handle error as needed

        elif current_route == "/profile":
            page.views.append(Profile(page))

        elif current_route == "/ai":
            ai = AI(page)
            ai.padding = 0
            page.views.append(ai)

        elif current_route == "/log_in":
            log_in = Log_in(page)
            log_in.padding = 0
            page.views.append(log_in)

        page.update()

    page.on_route_change = router
    page.go("/")

from urllib.parse import urlparse, parse_qs

class Uri:
    def __init__(self, route):
        self.route = route
        self._parsed_url = urlparse(route)
        self.query_params = parse_qs(self._parsed_url.query)

    @property
    def path(self):
        return self._parsed_url.path

    @staticmethod
    def parse(route):
        return Uri(route)


ft.app(main)
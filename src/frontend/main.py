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
from views.shop import Shop

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT    
    page.window.width = 375
    page.window.height = 667
    page.window.resizable = False
    page.update()

    def router(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(Landing(page))
    
        elif page.route == "/maps":
            maps = Maps(page)
            maps.padding = 0
            page.views.append(maps)

        elif page.route == "/favorite":
            page.views.append(Favorite(page))

        elif page.route == "/create":
            page.views.append(Create(page))  # Create usess API_URL

        elif page.route == "/questions":
            page.views.append(Questions(page))

        elif page.route == "/preference":
            page.views.append(Preference(page))

        elif page.route == "/about":
            about = About(page)
            about.padding = 0
            page.views.append(about)

        elif page.route == "/shop":
            shop = Shop(page)
            shop.padding = 0
            page.views.append(shop)

        elif page.route == "/profile":
            page.views.append(Profile(page))

        page.update()

    page.on_route_change = router
    page.go("/shop")   

ft.app(main)

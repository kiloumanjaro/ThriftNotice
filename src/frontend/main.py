import flet as ft
from views.landing import Landing
from views.maps import Maps
from views.favorite import Favorite
from views.options.questions import Questions  # Import from preference module
from views.create import Create
from views.preference import Preference
from views.about import About
from views.profile import Profile

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
            page.views.append(Create(page))

        elif page.route == "/questions":
            page.views.append(Questions(page))  # Use the initialized Preference view

        elif page.route == "/preference":
            page.views.append(Preference(page))  # Use the initialized Preference view

        elif page.route == "/about":
            page.views.append(About(page))

        elif page.route == "/profile":
            page.views.append(Profile(page))

        page.update()

    page.on_route_change = router
    page.go("/")   

ft.app(main)

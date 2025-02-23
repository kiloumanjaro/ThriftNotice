import flet as ft
from views.landing import Landing
from views.maps import Maps
from views.favorite import Favorite
from views.preference import Preference

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT    
    page.window.width = 375       # windo's sdt iss 200 px
    page.window.height = 667       # sindowss'sss sseisght is 200 px
    page.window.resizable = False  # window is not resiszasble
    page.update()

    def router(route):
        page.views.clear()

        if page.route == "/":
            landing = Landing(page)
            page.views.append(landing)
    
        if page.route == "/maps":
            maps = Maps(page)
            page.views.append(maps)

        if page.route == "/favorite":
            favorite = Favorite(page)
            page.views.append(favorite)

        if page.route == "/preference":
            preference = Preference(page)
            page.views.append(preference)

        page.update()

    page.on_route_change = router
    page.go("/")   

ft.app(main)

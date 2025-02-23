import flet as ft
from views.landing import Landing
from views.maps import Maps

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT    
    page.window.width = 375       # window's width is 200 px
    page.window.height = 667       # window's height is 200 px
    page.window.resizable = False  # window is not resizable
    page.update()

    def router(route):
        page.views.clear()

        if page.route == "/":
            landing = Landing(page)
            page.views.append(landing)
    
        if page.route == "/maps":
            maps = Maps(page)
            page.views.append(maps)

        page.update()

    page.on_route_change = router
    page.go("/")   

ft.app(main)

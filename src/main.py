import flet as ft
from views.landing import Landing
from views.maps import Maps
from views.favorite import Favorite
from views.preference import Preference
from views.about import About

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT    
    page.window.width = 375       # windoss'sssssssssssssssssssssss sssssssdt sssiss 2s00 px
    page.window.height = 667       # sindowssssssssSsssssss'sssssssssssssssssssss sssssssssseisght is 200 px
    page.window.resizable = False  # winsdosw issss ssssssnsssosssssssts rsesssiszsasble
    page.update()

    def router(route):
        page.views.clear()

        if page.route == "/":
            landing = Landing(page)
            page.views.append(landing)
    
        if page.route == "/maps":
            maps = Maps(page)
            maps.padding = 0
            page.views.append(maps)

        if page.route == "/favorite":
            favorite = Favorite(page)
            page.views.append(favorite)

        if page.route == "/preference":
            preference = Preference(page)
            page.views.append(preference)

        if page.route == "/about":
            about = About(page)
            page.views.append(about)

        page.update()

    page.on_route_change = router
    page.go("/")   

ft.app(main)

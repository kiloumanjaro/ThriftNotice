import flet as ft

class Landing(ft.View):
    def __init__(self, page: ft.Page): 
        super(Landing, self).__init__(
            route="/", horizontal_alignment="center",
            vertical_alignment="center"
        )

        self.page = page

        self.tab_logo = ft.Icon(name="shopping_cart_outlined", size=64)
        self.title = ft.Text("THRIFT NOTICE".upper(), size=28, weight="bold")
        self.subtitle = ft.Text("by TBA", size=11)

        self.maps_page_btn: Any = ft.IconButton(
            "arrow_forward", 
            width=54,
            height=54,
            style=ft.ButtonStyle(
                bgcolor={"": "#202020"},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                side={"": ft.BorderSide(2, "white54")},
            ),
            on_click=lambda e: self.page("/maps")
        )

        self.controls = [
            self.tab_logo, 
            ft.Divider(height=25, color="transparent"),
            self.title,
            self.subtitle,
            ft.Divider(height=10, color="transparent"),
            self.maps_page_btn,

        ]



# define the map page ...
class Maps(ft.View):
    def __init__(self, page: ft.Page):
        super(Maps, self).__init__(route="/maps")
        self.page = page

    def initialize(self):
        self.controls = [
            self.display_maps_page_header(),
            ft.Text("Shop", size=32),
            ft.Text("Select items from the list below"),
            self.display_maps_page_footer(),
        ]

    def display_map_page_footer(self):
        return ft.Row([ft.Text("Trift Notice", size="10")], alignment="center")

    def display_map_page_header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(name="settings", size=18),
                    ft.IconButton(
                        icon="shopping_cart_outlined",  
                        on_click=lambda e: self.page.go("/tab"),
                        icon_size=18,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN  
            )
        )



def main(page: ft.Page):

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

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
                bgcolor={"": "#FFFFFF"},
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                side={"": ft.BorderSide(2, "white54")},
            ),
            on_click=lambda e: self.page.go("/maps") 
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

        first_page_contents = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(alignment='spaceBetween',
                        controls=[
                            ft.Container(on_click=self.shrink,
                                content=ft.Icon(
                                    ft.icons.MENU)
                            ),
                            ft.Container(
                                content=ft.Icon(
                                    ft.icons.SEARCH)
                            )
                        ]
                    ),
                    ft.Divider(height=20, color="transparent"),
                    ft.Text(
                        value='What\'s up, Kint!'
                    ),
                    ft.Text(
                        value='CATEGORIES'
                    ),
                    ft.Container(
                        padding=ft.padding.only(top=10, bottom=20,),
                    )
                    
                ]
            )
        )
        
        self.page_1 = ft.Container()
        self.page_2 = ft.Row(
            controls=[
                ft.Container(
                    width=400,
                    height=850,
                    bgcolor='red',
                    border_radius=35,
                    animate=ft.animation.Animation(600, ft.AnimationCurve.DECELERATE),
                    animate_scale=ft.animation.Animation(400, curve='decelerate'),
                    padding=ft.padding.only(
                        top=50, left=20, right=20, bottom=5,
                    ),
                    content=ft.Column(
                        controls=[
                            first_page_contents
                        ]
                    )
                )
            ]
        )
        self.initialize() 

    def shrink(self, e):
        self.page_2.controls[0].width = 120
        self.page_2.update()

    def initialize(self):
        self.controls = [
            self.display_map_page_header(),
            ft.Text("Shop", size=32),
            ft.Text("Select items from the list below"),
            self.display_map_container(),
            self.display_map_page_footer(), 
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



    def display_map_container(self):
        return ft.Container(width=400, height=850, bgcolor='green', border_radius=35, 
        content=ft.Stack(
            controls=[
                self.page_1,
                self.page_2
            ]
        )
    )

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT    


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

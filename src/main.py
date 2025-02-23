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
                                    ft.Icons.MENU)
                            ),
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.SEARCH)
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
        
        self.page_1 = ft.Container( 
            bgcolor='green',
            border_radius=35,
            padding=ft.padding.only(left=50, top=60, right=200),
            content=ft.Column(  
                controls=[
                    ft.Container(
                        border_radius=25, padding=ft.padding.only(top=13, left=20),
                        height=50,
                        width=50,
                        border=ft.border.all(color='white', width=1),  
                        on_click=self.restore,
                        content=ft.Text('<')
                    )
                ]
            )
        )

        self.page_2 = ft.Row(alignment='end',
            controls=[
                ft.Container(
                    width=340,
                    bgcolor='red',
                    border_radius=35,
                    animate=ft.animation.Animation(600, ft.AnimationCurve.DECELERATE),
                    animate_scale=ft.animation.Animation(400, curve='decelerate'),
                    padding=ft.padding.only(
                        top=50, left=20, right=20, bottom=50,
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
        self.page_2.controls[0].scale = ft.transform.Scale(
            scale=0.8,  # Keep width the same
            alignment=ft.alignment.center_right)
        self.page_2.controls[0].border_radius=ft.border_radius.only(
            top_left = 35,
            top_right = 0,
            bottom_left = 35,
            bottom_right = 0
        )
        self.page_2.update()

    def restore(self, e):
        self.page_2.controls[0].width = 340
        self.page_2.controls[0].scale = ft.transform.Scale(
            1, alignment=ft.alignment.center_right)
        self.page_2.update()

    def initialize(self):
        self.controls = [
            self.display_map_container(),
        ]   

    def display_map_container(self):
        return ft.Container(expand=True, bgcolor='green', border_radius=35, 
        content=ft.Stack(
            controls=[
                self.page_1,
                self.page_2
            ]
        )
    )

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

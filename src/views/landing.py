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

        self.maps_page_btn: ft.Any = ft.IconButton(
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



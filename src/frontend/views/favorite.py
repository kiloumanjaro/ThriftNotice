import flet as ft

class Favorite(ft.View):
    def __init__(self, page: ft.Page): 
        super(Favorite, self).__init__(route="/favorite")
        self.page = page
        self.shop_container = self.create_shop()
        self.initialize()

    def initialize(self):
        self.controls = [self.display_shop_container()]

    def create_shop(self):
        container = ft.Container(
            width=375,
            height=575,
            padding=10,
            content=ft.Column(
                height=400,
                scroll="auto",
                controls=[ft.Container(width=300, height=50, bgcolor="red", border_radius=25)]
            ),
        )

        for i in range(10):
            container.content.controls.append(
                ft.Container(width=300, height=70, bgcolor="pink", border_radius=25)
            )

        return container  

    def display_shop_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("FAVORITE SHOPS", size=18, weight="bold"),
                    ft.Stack(
                        controls=[
                            self.shop_container,  # Reference pre-created task container
                            ft.FloatingActionButton(
                                bottom=2, right=20,
                                icon=ft.icons.ADD,
                                on_click=lambda e: self.page.go("/maps"),
                            )
                        ]
                    )
                ]
            )
        )

import flet as ft

class Favorite(ft.View):
    def __init__(self, page: ft.Page): 
        super(Favorite, self).__init__(route="/favorite")
        self.page = page
        self.shop_container = self.create_shop()
        self.initialize()

    def initialize(self):
        self.controls = [self.display_shop_container()]

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def create_shop(self):
        container = ft.Container(
            width=375,
            height=575,
            padding=ft.padding.symmetric(horizontal=20),
            content=ft.Column(
                height=400,
                scroll="auto",
                controls=[]
            ),
        )

        for i in range(10):
            shop_item = ft.Container(
                width=350,
                height=50,
                bgcolor="pink",  
                border_radius=5,
                padding=ft.padding.symmetric(horizontal=20, vertical=5),
                opacity=0.7,  
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.icons.STORE, color="black", size=16),  
                        ft.Text(f"Shop {i+1}", size=14, color="black", weight="bold"),
                    ],
                    alignment="start",
                ),
            )
            container.content.controls.append(shop_item)

      
        container.content.controls.append(ft.Container(height=30))  #SPACE

        return container  

    def display_shop_container(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Back Button + Title in the same row
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back_to_maps,
                                icon_color="black",  
                                style=ft.ButtonStyle(
                                    shape=None,  
                                    padding=ft.padding.all(10),
                                )
                            ),
                            ft.Text("FAVORITE SHOPS", size=18, weight="bold"),
                        ],
                        alignment="start", 
                    ),

                    # Shop List & FAB Button
                    ft.Stack(
                        controls=[
                            self.shop_container,
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

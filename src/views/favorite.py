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

    def toggle_details(self, e, details_container):
        details_container.visible = not details_container.visible
        self.page.update()

    def create_shop(self):
        container = ft.Container(
            expand=True,  
            padding=ft.padding.symmetric(horizontal=0),  
            content=ft.Column(
                expand=True,
                scroll="auto",
                controls=[]
            ),
        )

        for i in range(10):
            details_container = ft.Container(
                visible=False,  
                content=ft.Column(
                    controls=[
                        ft.Text("📍 Location: Sample Address", size=12, color="black"),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.STAR, color="gold", size=16),
                                ft.Icon(ft.icons.STAR, color="gold", size=16),
                                ft.Icon(ft.icons.STAR, color="gold", size=16),
                                ft.Icon(ft.icons.STAR, color="gold", size=16),
                                ft.Icon(ft.icons.STAR_BORDER, color="gold", size=16),
                            ],
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=5),
                bgcolor="white",
                border_radius=5
            )

            shop_item = ft.Container(
                bgcolor="white",
                border_radius=10,  
                padding=ft.padding.symmetric(vertical=3, horizontal=10), 
                margin=ft.margin.symmetric(vertical=3, horizontal=15), 
                content=ft.Column(
                    controls=[
                        ft.Container(
                            height=40,  
                            bgcolor="#98e2f6",
                            border_radius=8, 
                            padding=ft.padding.symmetric(horizontal=15, vertical=3),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name=ft.icons.STORE, color="black", size=14), 
                                    ft.Text(f"Shop {i+1}", size=13, color="black", weight="regular"),  
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_DROP_DOWN,
                                        icon_color="black",  
                                        style=ft.ButtonStyle(
                                            bgcolor="transparent",  
                                            overlay_color="transparent",
                                        ),
                                        on_click=lambda e, d=details_container: self.toggle_details(e, d),
                                    ),
                                ],
                                alignment="spaceBetween",
                            ),
                        ),
                        details_container,  
                    ],
                ),
            )

            container.content.controls.append(shop_item)

        return container

    def display_shop_container(self):
        return ft.Column(
            expand=True,  
            controls=[
                ft.Container(
                    bgcolor="#5f82a6",
                    border_radius=15,  
                    padding=ft.padding.symmetric(vertical=12, horizontal=20),
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back_to_maps,
                                icon_color="black",
                            ),
                            ft.Text("Favorite Shops", size=18, weight="bold", color="#f8f9ff"),
                            ft.Icon(  
                                name=ft.icons.FAVORITE,  
                                color="#FF6347",
                                size=20
                            ),
                        ],
                        alignment="spaceBetween",
                    ),
                ),
                ft.Stack(
                    expand=True,
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

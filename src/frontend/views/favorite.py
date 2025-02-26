import flet as ft

class Favorite(ft.View):
    def __init__(self, page: ft.Page):
        super(Favorite, self).__init__(route="/favorite")
        self.bg = '#1c1c1c'
        self.fg = '#98e2f6'
        self.wg = '#f8f9ff'
        self.fg1 = '#5f82a6'
        self.bg1 = '#323232'
        self.page = page
        self.shop_container = self.create_shop()
        self.initialize()
        self.bgcolor = self.bg

    def initialize(self):
        self.controls = [self.display_shop_container()]

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def toggle_details(self, e, details_container, shop_item, shop_header, icon_button, shop_text):
        details_container.visible = not details_container.visible
        icon_button.icon = ft.icons.ARROW_DROP_DOWN if details_container.visible else ft.icons.ARROW_DROP_UP

        # Update background colors when expanded/collapsed
        icon_button.icon_color = "black" if details_container.visible else "white"
        new_bgcolor = "#98e2f6" if details_container.visible else self.bg1
        text_color = "black" if details_container.visible else "white"

        details_container.bgcolor = new_bgcolor
        shop_item.bgcolor = new_bgcolor
        shop_header.bgcolor = new_bgcolor  

        # Update the shop text color
        shop_text.color = text_color

        self.page.update()


    def create_toggle_button(self, details_container, shop_item, shop_header, shop_text):
        icon_button = ft.IconButton(
            icon=ft.icons.ARROW_DROP_UP,  
            icon_color="white",
            style=ft.ButtonStyle(
                bgcolor="transparent",
                overlay_color="transparent",
            ),
        )

        def toggle_details_handler(e):
            self.toggle_details(e, details_container, shop_item, shop_header, icon_button, shop_text)

        icon_button.on_click = toggle_details_handler
        return icon_button

    def create_shop(self):
        container = ft.Container(
            expand=True,
            padding=ft.padding.symmetric(horizontal=0),
            content=ft.Column(expand=True, scroll="always", controls=[]),  # Ensure scrollbar is always visibl
        )

        for i in range(4):
            details_container = ft.Container(
                visible=False,
                content=ft.Column(
                    controls=[
                        ft.Text("Sample Address", size=12, color="black", italic=True),
                    ],
                ),
                padding=ft.padding.only(left=15, right=20, top=0, bottom=15),
                bgcolor=self.bg1,
                border_radius=5
            )

            shop_item = ft.Container(
                bgcolor=self.bg1,
                border_radius=10,
                padding=ft.padding.symmetric(vertical=3, horizontal=10),
                margin=ft.margin.symmetric(vertical=3, horizontal=15),
            )

            shop_header = ft.Container(
                height=40,
                bgcolor=self.bg1,  
                border_radius=8,
                padding=ft.padding.only(left=15, right=3, top=3, bottom=3),
            )

            # Shop title text (so we can modify its color dynamically)
            shop_text = ft.Text(f"Shop {i+1}", size=13, color="white")

            # Create toggle button with updated reference
            icon_button = self.create_toggle_button(details_container, shop_item, shop_header, shop_text)

            shop_header.content = ft.Row(
                controls=[
                    shop_text,  # Forces text to the left
                    ft.Container(
                        content=icon_button,
                        alignment=ft.alignment.center_right,  # Ensures button is fully to the right
                    ),
                ],
                alignment="spaceBetween",
            )

            shop_item.content = ft.Column(
                controls=[
                    shop_header,  
                    details_container,
                ],
                spacing=0,
            )

            container.content.controls.append(shop_item)

        return container
    def display_shop_container(self):
        return ft.Column(
            height=700,
            scroll="auto",  # Allow scrolling for this section
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=self.go_back_to_maps,
                            style=ft.ButtonStyle(
                                shape={"": ft.CircleBorder()},
                                padding=ft.padding.all(5),
                                bgcolor=self.bg,
                                color="white",
                            )
                        ),
                        ft.Container(
                            padding=ft.padding.only(left=83),
                            content=ft.Text("Favorites", size=16, weight=ft.FontWeight.BOLD, color='white'),
                            alignment=ft.alignment.center
                        ),
                    ],
                    alignment="start",
                ),
                ft.Container(
                    alignment=ft.alignment.center,  # Centers the icon
                    padding=ft.padding.only(top=12, bottom=28),  # Adds spacing
                    content=ft.Icon(ft.icons.STORE, color="white", size=180)  # Large favorite icon
                ),
                ft.Container(
                    height=323,  
                    content=ft.Stack(
                        expand=True,
                        controls=[
                            self.shop_container,  
                            # Floating Action Button
                            ft.FloatingActionButton(
                                
                                bottom=2, right=20,
                                icon=ft.icons.ADD,
                                on_click=lambda e: self.page.go("/maps"),
                                bgcolor="white",
                                foreground_color=self.bg,
                                shape=ft.CircleBorder()
                            )
                        ]
                    ),
                )
            ]
        )
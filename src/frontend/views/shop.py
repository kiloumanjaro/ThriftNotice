import flet as ft

class Shop(ft.View):
    def __init__(self, page: ft.Page):
        super(Shop, self).__init__(route="/shop", padding=0, bgcolor='white')
        self.page = page
        self.shop_name = "Shop Name"
        self.formatted_address = "123 Vintage Lane, Suite 5, Brookville, USA"
        self.short_description = (
            "Nestled in the heart of the city, Timeless Treasures Thrift Shop is a hidden gem for bargain hunters and "
            "vintage lovers alike. Our shop offers a carefully curated selection of pre-loved clothing, unique home décor, "
            "rare collectibles, and secondhand books—all at unbeatable prices. Whether you're searching for a one-of-a-kind "
            "fashion statement, a nostalgic keepsake, or simply a great deal, our ever-changing inventory has something for everyone."
        )
        self.reviews = ["Great shop!", "Nice collection!", "Affordable and unique items."]
        self.is_favorite = False

        self.initialize()

    def initialize(self):
        self.controls = [self.display_shop_container()]

    def toggle_favorite(self, e):
        self.is_favorite = not self.is_favorite
        self.favorite_button.icon = ft.icons.FAVORITE if self.is_favorite else ft.icons.FAVORITE
        self.favorite_button.icon_color = "red" if self.is_favorite else "#323232"
        self.favorite_button.update()
        self.page.update()

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def display_shop_container(self):
        self.favorite_button = ft.IconButton(
            icon=ft.icons.FAVORITE,
            icon_size=20,
            icon_color="#323232",
            on_click=self.toggle_favorite,
        )

        self.review_items = [
            ft.Container(
                bgcolor="#f8f9ff",
                padding=8,
                border_radius=10,
                border=ft.border.all(0.5, "black"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30),
                        ft.Text(review, size=12, color="black"),
                    ],
                    spacing=10,
                )
            )
            for review in self.reviews
        ]

        return ft.Container(
            expand=True,
            padding=ft.padding.only(bottom=10),
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        top=0,
                        border=ft.border.all(0.5, "black"),
                        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
                        content=ft.Container(
                            alignment=ft.alignment.center,
                            content=ft.Image(
                                src="cyres.jpg",
                                width=380,
                                height=280,
                                fit=ft.ImageFit.COVER,
                            ),
                        ),
                    ),
                    ft.Container(
                        top=220,
                        width=360,
                        height=500,
                        bgcolor="white",
                        padding=ft.padding.only(left=25, right=25, top=20),
                        border_radius=ft.border_radius.only(top_left=20, top_right=20),
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(self.shop_name, size=23, weight="bold", color="black"),
                                ft.Text(self.formatted_address, size=10, color="black"),
                                ft.Divider(height=5, color="transparent"),
                                ft.Text("Community Reviews", size=10, color="black"),
                                ft.Container(
                                    expand=True,
                                    padding=ft.padding.only(top=5),
                                    content=ft.Column(controls=self.review_items)
                                )
                            ]
                        ),
                    ),
                    # Favorite icon inside a circular background
                    ft.Container(
                        top=197,
                        right=35,
                        width=45,
                        height=45,
                        bgcolor="white",
                        border_radius=50,
                        border=ft.border.all(0.5, "#1c1c1c"),
                        alignment=ft.alignment.center,
                        content=self.favorite_button
                    ),
                    # Floating button for maps
                    ft.Container(
                        bottom=10,
                        right=35,
                        width=50,
                        height=50,
                        bgcolor="#1c1c1c",
                        border_radius=50,
                        alignment=ft.alignment.center,
                        content=ft.IconButton(
                            icon=ft.icons.MAP,
                            icon_size=20,
                            icon_color="white",
                            on_click=self.go_back_to_maps
                        )
                    ),
                ]
            ),
        )
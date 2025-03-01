import flet as ft

class Shop(ft.View):

    def __init__(self, page: ft.Page): 
        super(Shop, self).__init__(route="/shop", padding=0)
        self.page = page
        self.shop_name = 'Shop Name'
        self.formatted_address = '123 Vintage Lane, Suite 5, Brookville, USA'
        self.short_description = (
            "Nestled in the heart of the city, Timeless Treasures Thrift Shop is a hidden gem for bargain hunters and "
            "vintage lovers alike. Our shop offers a carefully curated selection of pre-loved clothing, unique home décor, "
            "rare collectibles, and secondhand books—all at unbeatable prices. Whether you're searching for a one-of-a-kind "
            "fashion statement, a nostalgic keepsake, or simply a great deal, our ever-changing inventory has something for everyone."
        )
        self.reviews = ["Great shop!", "Nice collection!", "Affordable and unique items."]  # List of review texts
        self.is_favorite = False  # Track favorite state
        self.initialize()

    def initialize(self):
        self.controls = [self.display_shop_container()]

    def toggle_favorite(self, e):
        self.is_favorite = not self.is_favorite
        self.favorite_button.icon = ft.icons.FAVORITE if self.is_favorite else ft.icons.FAVORITE_BORDER
        self.favorite_button.icon_color = "red" if self.is_favorite else "black"
        self.favorite_button.update()

    def go_back_to_maps(self, e):
        self.page.go("/maps")
        self.page.update()

    def display_shop_container(self): 
        # Fix missing closing parenthesis
        self.favorite_button = ft.IconButton(
            icon=ft.icons.FAVORITE_BORDER,
            icon_size=20,
            icon_color="black",  # Keep icon color black
            on_click=self.toggle_favorite,
        )

        # Generate review items correctly
        self.review_items = [
            ft.Container(
                bgcolor="#f1f1f1",
                padding=8,
                border_radius=10,
                border=ft.border.all(0.5, "black"),  # Border with 1px thickness and black color
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=30),  # Profile icon
                        ft.Text(review, size=12),  # Review text
                    ],
                    spacing=10,
                )
            )
            for review in self.reviews  # <-- Loop is placed correctly here
        ]

        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                scroll="auto",  # Enable scrolling
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor="white",
                        padding=10,
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    on_click=self.go_back_to_maps,
                                    style=ft.ButtonStyle(
                                        shape={"": ft.CircleBorder()},
                                        padding=ft.padding.all(5),
                                        bgcolor="white",
                                        color="#1c1c1c",
                                    )
                                ),
                                ft.Container(
                                    padding=ft.padding.only(left=96),
                                    content=ft.Text("Shop", size=16, weight=ft.FontWeight.BOLD, color="black"),
                                    alignment=ft.alignment.center
                                ),
                            ], alignment="start",
                        )
                    ),
                    
                    # Added image with borders
                    ft.Container(
                        padding=ft.padding.only(left=10, right=10, bottom=10, top=0),
                        content=ft.Image(src="cyres.jpg"),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        expand=True,
                        padding=ft.padding.only(left=30, right=30),
                        content=ft.Column(
                            expand=True,
                            spacing=10,
                            scroll="auto",
                            controls=[
                                ft.Row(
                                    alignment="spaceBetween",
                                    controls=[
                                        ft.Text(self.shop_name, size=23, weight="bold"),
                                        self.favorite_button,
                                    ],
                                ),
                                ft.Text(self.formatted_address, size=10),
                                ft.Text(self.short_description, size=12),
                                ft.Divider(height=5, color="transparent"),
                                ft.Text("Community Reviews", size=14, weight="bold"),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        padding=ft.padding.only(left=25, right=25),
                        content=ft.Column(controls=self.review_items)
                    )
                    
                ]
            )
        )

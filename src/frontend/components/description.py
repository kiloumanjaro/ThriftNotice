import flet as ft

class BottomSheet(ft.Container):
    def __init__(self, on_close):
        self.shop_name = 'Shop Name'  # Define instance variable
        self.formatted_address = '123 Vintage Lane, Suite 5, Brookville, USA'  # Define instance variable
        self.short_description = "Nestled in the heart of the city, Timeless Treasures Thrift Shop is a hidden gem for bargain hunters and vintage lovers alike. Our shop offers a carefully curated selection of pre-loved clothing, unique home décor, rare collectibles, and secondhand books—all at unbeatable prices. Whether you're searching for a one-of-a-kind fashion statement, a nostalgic keepsake, or simply a great deal, our ever-changing inventory has something for everyone."

        super().__init__(
            width=318,
            height=360,  # Adjusted height
            bgcolor="white",
            border_radius=ft.border_radius.all(20),
            margin=ft.margin.only(bottom=23),
            padding=ft.padding.only(top=10, bottom=20, right=15, left=25),
            bottom=-400,  # Initially hidden below the screen
            animate_position=ft.animation.Animation(400, "decelerate"),
            shadow=ft.BoxShadow(
                spread_radius=1,  # Reduced spread
                blur_radius=3,  # Softer shadow
                color=ft.colors.BLACK12,  # Lighter shadow
                offset=ft.Offset(0, 1)  # Minimal vertical offset
            ),  
            content=ft.Column(
                expand=True,  # Makes the column take full height
                controls=[
                    ft.Row( 
                        alignment='spaceBetween',
                        controls=[
                            ft.Text(self.shop_name, size=23, weight='bold'),
                            ft.IconButton(ft.icons.CLOSE, on_click=on_close, icon_size=20),
                        ]
                    ),
                    ft.Container(
                        padding=ft.padding.only(right=15),
                        content=ft.Column(
                            controls=[
                                ft.Text(self.formatted_address, size=10),
                                ft.Text(
                                    self.short_description,
                                    size=12
                                ),
                            ]                        
                        )
                    ),
                    # TextField with Submit button
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=220,
                                content=ft.TextField(
                                    hint_text="Write a review...",
                                    text_style=ft.TextStyle(size=12, color="gray"),
                                    border_radius=10,
                                    height=40
                                )
                            ),
                            ft.IconButton(
                                icon=ft.icons.SEND,
                                icon_size=20,
                                tooltip="Submit Review"
                            )
                        ]
                    )
                ]
            )
        )

    def show(self):
        self.bottom = 0
        self.update()
    
    def hide(self):
        self.bottom = -400
        self.update()

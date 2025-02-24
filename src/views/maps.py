import flet as ft
from components.description import BottomSheet

class Maps(ft.View):
    def __init__(self, page: ft.Page):
        name = 'Kint Louise Borbano'
        super(Maps, self).__init__(route="/maps")
        self.page = page

        self.bottom_sheet = BottomSheet(self.close_bottom_sheet)
        self.search_bar = ft.Container(
            width=50,  # Collapsed width
            height=40,
            border=None,
            border_radius=20,
            bgcolor="red",
            padding=ft.padding.only(right=20),
            animate=ft.animation.Animation(400, "decelerate"),
            content=ft.Row(
                spacing=0,  # Set spacing to 0
                controls=[
                    ft.IconButton(ft.icons.SEARCH, on_click=self.toggle_search),
                    ft.TextField(
                        hint_text=" Search",
                        text_style=ft.TextStyle(size=14, color="gray"), 
                        bgcolor="white",
                        border=None,
                        border_radius=25,
                        border_width=0,
                        expand=True,
                        visible=False,  # Initially hidden
                    ),
                ]
            )
        )

        self.fab = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            bgcolor="white",
            bottom=300,
            right=200,
            shape=ft.CircleBorder(),
            elevation=3,
            width=55,
            height=55,
            on_click=self.open_bottom_sheet
        )

        circle = ft.Stack(
            controls=[
                ft.Container(width=100, height=100, border_radius=50, bgcolor="white12"),
                ft.Container(
                    gradient=ft.SweepGradient(
                        center=ft.alignment.center,
                        start_angle=0.0,
                        end_angle=3,
                        stops=[0.5, 0.5],
                        colors=["#00000000", 'red'],
                    ),
                    width=100,
                    height=100,
                    border_radius=50,
                    content=ft.Row(
                        alignment="center",
                        controls=[
                            ft.Container(
                                padding=ft.padding.all(5),
                                bgcolor='green',
                                width=90,
                                height=90,
                                border_radius=50,
                                content=ft.Container(
                                    bgcolor='red',
                                    height=80,
                                    width=80,
                                    border_radius=40,
                                    content=ft.CircleAvatar(
                                        opacity=0.8,
                                        foreground_image_src="https://images.unsplash.com/photo-1545912452-8aea7e25a3d3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80",
                                    ),
                                ),
                            )
                        ],
                    ),
                ),
            ]
        )

        first_page_contents = ft.Container(
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Row(alignment='spaceBetween',
                        controls=[
                            ft.Container(on_click=self.shrink,
                                content=ft.Icon(ft.Icons.MENU)
                            ),
                            self.search_bar,  # Expandable search bar
                        ]
                    ),
                    ft.Divider(height=20, color="transparent"),
                    ft.Text(value="What's up, Kint!"),
                    ft.Text(value="MAP AND MAIN UI GOES HERE"),
                ]
            ),
            on_click=self.close_search,  # Detect clicks outside search bar
        )

        
        self.page_1 = ft.Container( 
            bgcolor='green',
            border_radius=0,
            padding=ft.padding.only(left=50, top=60, right=200),
            content=ft.Column(  
                controls=[
                    ft.Row(alignment='end',
                    controls=[ ft.Container(
                        border_radius=25, padding=ft.padding.only(top=13, left=20),
                        height=50,
                        width=50,
                        border=ft.border.all(color='white', width=1),  
                        on_click=self.restore,
                        content=ft.Text('<')
                        )
                    ]
                   ),
                    ft.Divider(height=25, color="transparent"),
                    circle,
                    ft.Text(name, size=20, weight='bold'),
                    ft.Divider(height=25, color="transparent"),
                    ft.TextButton(
                        text="Favorites",
                        icon=ft.icons.FAVORITE_BORDER_SHARP,
                        on_click=lambda e: self.page.go("/favorite"),
                        style=ft.ButtonStyle(
                            color="white",
                            padding=ft.padding.all(10)
                        )
                    ),
                    ft.TextButton(
                        text="Preference",
                        icon=ft.icons.CARD_TRAVEL,
                        on_click=lambda e: self.page.go("/preference"),
                        style=ft.ButtonStyle(
                            color="white",
                            padding=ft.padding.all(10)
                        )
                    ),
                    ft.TextButton(
                        text="About",
                        icon=ft.icons.CALCULATE_OUTLINED,
                        on_click=lambda e: self.page.go("/about"),
                        style=ft.ButtonStyle(
                            color="white",
                            padding=ft.padding.all(10)
                        )
                    ),
                ]
            )
        )

        self.page_2 = ft.Row(alignment='end',
            controls=[
                ft.Container(
                    width=375,
                    bgcolor='red',
                    border_radius=0,
                    animate=ft.animation.Animation(600, ft.AnimationCurve.DECELERATE),
                    animate_scale=ft.animation.Animation(400, curve='decelerate'),
                    padding=ft.padding.only(
                        top=12, left=22, right=17, bottom=0,
                    ),
                    content=ft.Stack(
                        controls=[
                            first_page_contents,
                            self.fab,
                            self.bottom_sheet
                        ]
                    )
                )
            ]
        )
        self.initialize() 

    def initialize(self):
        self.controls = [
            self.display_map_container(),
        ]   

    def open_bottom_sheet(self, e):
        self.bottom_sheet.show()

    def close_bottom_sheet(self, e):
        self.bottom_sheet.hide()

    def toggle_search(self, e):
        """Expands or collapses the search bar when the search icon is clicked."""
        text_field = self.search_bar.content.controls[1]
        if self.search_bar.width == 50:
            self.search_bar.width = 300  # Expand width
            text_field.visible = True  # Show input field
        else:
            self.close_search(e)  # Collapse if already expanded
        self.search_bar.update()



    def close_search(self, e):
        """Closes the search bar when clicking outside of it."""
        text_field = self.search_bar.content.controls[1]
        if self.search_bar.width > 50:  # Only close if expanded
            self.search_bar.width = 50
            text_field.visible = False
            self.search_bar.update()

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
        self.page_2.controls[0].padding=ft.padding.only(
            top=12,
            left=22,
            right=0, 
            bottom=10,
        )
        self.close_search(e)
        self.search_bar.update()
        self.bottom_sheet.hide()
        self.page_2.update()

    def restore(self, e):
        self.page_2.controls[0].width = 375
        self.page_2.controls[0].scale = ft.transform.Scale(
            1, alignment=ft.alignment.center_right)
        self.page_2.controls[0].border_radius=ft.border_radius.only(
            top_left = 0,
            top_right = 0,
            bottom_left = 0,
            bottom_right = 0
        )
        self.page_2.controls[0].padding=ft.padding.only(
            top=12,
            left=22,
            right=17, 
            bottom=10,
        )
        self.page_2.update()


    def display_map_container(self):
        return ft.Container(expand=True, bgcolor='green', border_radius=0, 
        content=ft.Stack(
            controls=[
                self.page_1,
                self.page_2,
            ]
        )
    )


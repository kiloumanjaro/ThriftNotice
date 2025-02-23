import flet as ft

class Maps(ft.View):
    def __init__(self, page: ft.Page):
        name = 'Kint Louise Borbano'
        super(Maps, self).__init__(route="/maps")
        self.page = page

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
                    ft.Text(name, size=32, weight='bold'),
                    ft.Divider(height=25, color="transparent"),
                    ft.Row(controls=[
                        ft.Icon(ft.icons.FAVORITE_BORDER_SHARP),
                        ft.Text('Favorites', size=15, weight=ft.FontWeight.W_300, color='white', font_family='poppins')
                    ]), 
                    ft.Row(controls=[
                        ft.Icon(ft.icons.CARD_TRAVEL),
                        ft.Text('Preference', size=15, weight=ft.FontWeight.W_300, color='white', font_family='poppins')
                    ]), 
                                        ft.Row(controls=[
                        ft.Icon(ft.icons.CALCULATE_OUTLINED),
                        ft.Text('About', size=15, weight=ft.FontWeight.W_300, color='white', font_family='poppins')
                    ]), 
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


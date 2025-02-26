                    content=ft.Stack(
                        expand=True,
                        controls=[
                            self.shop_container,
                            ft.Container(
                                    height=33,
                                content=ft.FloatingActionButton(
                                    icon=ft.icons.ADD,
                                    on_click=lambda e: self.page.go("/maps"),
                                    bgcolor="white",
                                    foreground_color=self.bg,
                                    shape=ft.CircleBorder(),
                                ),
                                alignment=ft.alignment.bottom_right,  # Fixes the button position
                                padding=ft.padding.only(bottom=20, right=20),  # Adjust spacing from edges
                            )
                        ]
                    ),
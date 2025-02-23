import flet as ft

class Favorite(ft.View):
    def __init__(self, page: ft.Page): 
        super(Favorite, self).__init__(route="/favorite")
        self.page = page

        # Wrapping the Column in a Container to apply bgcolor
        task_container = ft.Container(
            width=375,
            height=575,
            padding=10,
            content=ft.Column(
                height=400,
                scroll="auto",
                controls=[
                    ft.Container(width=300, height=50, bgcolor="red", border_radius=25),
                ]
            ),
        )

        # Adding additional tasks dynamically
        for i in range(10):
            task_container.content.controls.append(
                ft.Container(width=300, height=70, bgcolor="pink", border_radius=25)
            )

        table_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("TODAY'S TASKS", size=18, weight="bold"),
                    ft.Stack(
                        controls=[
                            task_container,  # Task list
                            ft.FloatingActionButton(
                                bottom=2, right=20,
                                icon=ft.icons.ADD,
                                on_click=lambda e: page.go("/maps"),
                            )
                        ]
                    )
                ]
            )
        )



        # Assigning to self.controls to render properly
        self.controls = [table_content]

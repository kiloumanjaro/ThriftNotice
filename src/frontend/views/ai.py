import flet as ft
from components.prompt import Prompt
import flet.map as map
import math
import os
import requests

class AI(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/ai")
        self.page = page
        # Define color scheme (only those in use)
        wg = '#f8f9ff'
        fg1 = '#5f82a6'

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        self.marker_data = {}
        self.marker_counter = 1
        self.prompt_sheet = Prompt(self.close_prompt_sheet) 


        def on_bottom_button_click(e):
            print("Bottom button clicked")  # Debugging
            self.page.go("/maps")

        self.bottom_button = ft.Container(
            margin=ft.margin.only(top=540),
            width=50,
            height=50,
            bgcolor="#323232",
            border_radius=50,
            alignment=ft.alignment.center,
            border=ft.border.all(3, "#98e2f6"),  # Add a 2px white border
            content=ft.IconButton(
                icon=ft.icons.HOME,
                icon_size=23,
                icon_color="white",
                on_click=on_bottom_button_click  # Move on_click here
            ),
        )


        def is_within_radius(coord1, coord2, radius):
            lat1, lon1 = coord1
            lat2, lon2 = coord2
            R = 6371000  # Earth radius in meters
            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)
            a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c < radius

        def get_initial_map_markers(e):
            locations_api_url = os.getenv("LOCATIONS_API_URL")
            response = requests.get(locations_api_url)
            if response.status_code == 200:
                locations_data = response.json()
                if marker_layer_ref.current is None or not hasattr(marker_layer_ref.current, 'markers'):
                    return
                marker_layer_ref.current.markers.clear()
                for location in locations_data:
                    latitude = location.get('latitude')
                    longitude = location.get('longitude')
                    if latitude is not None and longitude is not None:
                        try:
                            latitude = float(latitude)
                            longitude = float(longitude)
                            marker = map.Marker(
                                content=ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED, size=25),
                                coordinates=map.MapLatitudeLongitude(latitude, longitude),
                                data={"shopid": location['shopid']}
                            )
                            marker_layer_ref.current.markers.append(marker)
                        except (ValueError, TypeError):
                            pass
                marker_layer_ref.current.update()
            else:
                print(f"Error fetching map locations: {response.status_code}")

        def handle_tap(e: map.MapTapEvent):
            coordinates = (e.coordinates.latitude, e.coordinates.longitude)
            # Check if tap is near an existing marker
            for marker in marker_layer_ref.current.markers:
                marker_coords = (marker.coordinates.latitude, marker.coordinates.longitude)
                if is_within_radius(marker_coords, coordinates, radius=30):
                    for m in marker_layer_ref.current.markers:
                        m.content = ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED, size=25)
                    marker.content = ft.Icon(ft.icons.LOCATION_ON, color="blue", size=40)
                    marker_layer_ref.current.update()
                    cebu.center_on(
                        map.MapLatitudeLongitude(marker.coordinates.latitude * 0.999763, marker.coordinates.longitude),
                        zoom=16.6
                    )
                    self.open_prompt_sheet(e)
                    return

            # Prevent adding a marker too close to an existing one
            for marker_id, coord in self.marker_data.items():
                if is_within_radius(coord, coordinates, radius=30):
                    print(f"Too close to marker ID {marker_id}, cannot place here!")
                    return

            marker_id = self.marker_counter
            self.marker_counter += 1
            self.marker_data[marker_id] = coordinates

            marker_layer_ref.current.markers.append(
                map.Marker(
                    content=ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED, size=25),
                    coordinates=e.coordinates,
                )
            )
            marker_layer_ref.current.update()
            print(f"Added marker ID: {marker_id} at {coordinates}")

        cebu = map.Map(
            expand=True,
            initial_zoom=14.5,
            initial_center=map.MapLatitudeLongitude(10.3055, 123.8938),
            interaction_configuration=map.MapInteractionConfiguration(flags=map.MapInteractiveFlag.ALL),
            on_init=get_initial_map_markers,
            on_tap=handle_tap,
            on_secondary_tap=handle_tap,
            on_long_press=handle_tap,
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                map.MarkerLayer(
                    ref=marker_layer_ref,
                    markers=[
                        map.Marker(
                            content=ft.Icon(ft.Icons.LOCATION_ON),
                            coordinates=map.MapLatitudeLongitude(30, 15),
                        ),
                        map.Marker(
                            content=ft.Icon(ft.Icons.LOCATION_ON),
                            coordinates=map.MapLatitudeLongitude(10, 10),
                        ),
                        map.Marker(
                            content=ft.Icon(ft.Icons.LOCATION_ON),
                            coordinates=map.MapLatitudeLongitude(25, 45),
                        ),
                    ],
                ),
            ]
        )

        first_page_contents = ft.Container(
            expand=True,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        content=ft.Container(
                            expand=True,
                            content=cebu,
                            width=375,
                            height=667,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        )
                    )
                ]
            ),
        )

        self.page_2 = ft.Row(
            alignment='end',
            controls=[
                ft.Container(
                    width=375,
                    bgcolor=wg,
                    content=ft.Stack(height=667, controls=
                                     [first_page_contents, 
                                        ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[self.bottom_button],  # Wrap in a list
                                        ),
                                         self.prompt_sheet])
                )
            ]
        )
        self.initialize()

    def initialize(self):
        self.controls = [self.display_map_container()]

    def open_prompt_sheet(self, e):
        self.prompt_sheet.show()

    def close_prompt_sheet(self, e):
        self.prompt_sheet.hide()

    def display_map_container(self):
        return ft.Container(
            expand=True,
            content=ft.Stack(expand=True, controls=[self.page_2])
        )

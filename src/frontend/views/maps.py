import flet as ft
from components.description import BottomSheet
import flet.map as map
import math
import os
import requests
import json
import hashlib

class Maps(ft.View):
    def __init__(self, page: ft.Page):
        super(Maps, self).__init__(route="/maps")
        self.page = page
        self.name = self.page.session.get("username") or "Guest-101"
        self.is_shrunk = False
        bg='#1c1c1c'
        fg='#98e2f6'
        wg='#f8f9ff'
        fg1='#5f82a6'

        def is_within_radius(coord1, coord2, radius):  # Radius in meters
            lat1, lon1 = coord1
            lat2, lon2 = coord2
            R = 6371000  # Earth radius in meters

            phi1, phi2 = math.radians(lat1), math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)

            a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            distance = R * c  # Distance in meters
            return distance < radius  # Returns True if inside restricted radius

        self.bottom_sheet = BottomSheet(self.close_bottom_sheet)
        self.search_bar = ft.Container(
            width=50,  # Collapsed width
            height=40,
            border=None,
            border_radius=20,
            bgcolor=wg,
            padding=ft.padding.only(right=18),
            animate=ft.animation.Animation(400, "decelerate"),
            content=ft.Row(
                spacing=0,  # Set spacing to 0
                controls=[
                    ft.IconButton(ft.icons.SEARCH, on_click=self.toggle_search, icon_color=fg1),
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

        # Define the main circular stack
        circle = ft.Stack(
            controls=[
                ft.Container(width=100, height=100, border_radius=50, bgcolor="white12"),
                ft.Container(
                    gradient=ft.SweepGradient(
                        center=ft.alignment.center,
                        start_angle=0.0,
                        end_angle=3,
                        stops=[0.5, 0.5],
                        colors=["#00000000", fg],
                    ),
                    width=100,
                    height=100,
                    border_radius=50,
                    content=ft.Row(
                        alignment="center",
                        controls=[
                            ft.Container(
                                padding=ft.padding.all(5),
                                bgcolor=bg,
                                width=90,
                                height=90,
                                border_radius=50,
                                content=ft.Container(
                                    bgcolor=bg,
                                    height=80,
                                    width=80,
                                    border_radius=40,
                                    content=ft.CircleAvatar(
                                        bgcolor='#1c1c1c',
                                        content=ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=80, color=wg)
                                    ),
                                ),
                            )
                        ],
                    ),
                ),
            ]
        )

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        self.marker_data = {}  # Dictionary to store marker id and coordinates
        self.marker_counter = 1  # Counter to assign unique IDs

        def get_initial_map_markers(e):
            """Fetches map markers from API, adds them to marker_layer."""
            locations_api_url = os.getenv("LOCATIONS_API_URL")  # API URL from environment

            stored_data_hash = self.page.session.get("db_state_hash") # Retrieve stored hash
            stored_marker_layer = self.page.session.get("marker_layer") # Retrieve stored marker layer

            if stored_data_hash and stored_marker_layer: # Check if both hash and marker layer are stored
                print("Stored marker layer found. Checking database state...")
                response = requests.get(locations_api_url) # Fetch current data to check hash
                if response.status_code == 200:
                    current_data_hash = hashlib.sha256(response.content).hexdigest()
                    if current_data_hash == stored_data_hash:
                        print("Database state unchanged, loading stored marker layer.")
                        marker_layer_ref.current.markers = stored_marker_layer # Load stored marker layer
                        marker_layer_ref.current.update()
                        return # Skip API data fetch and marker creation
                    else:
                        print("Database state changed. Fetching new markers from API.")
                else:
                    print(f"Warning: Could not verify database state. Fetching new markers anyway. API error: {response.status_code}")


            response = requests.get(locations_api_url)  # Fetch data from API if no stored layer or hash mismatch

            if response.status_code == 200:  # API call successful
                try:
                    locations_data = response.json()  # Parse JSON response
                    current_data_hash = hashlib.sha256(response.content).hexdigest() # Generate hash of the current data

                except json.JSONDecodeError:
                    print(f"Error decoding JSON from API response: {response.text}")
                    print(f"Status code: {response.status_code}")
                    return

                except Exception as ex: # Catch other potential errors during API processing
                    print(f"An error occurred during API processing: {ex}")
                    return

                print(f"Locations Data from API: {locations_data}")
                print(f"Type of locations_data: {type(locations_data)}")

                if marker_layer_ref.current is None:
                    print("Error: marker_layer_ref.current is None. Map init issue.")
                    return
                if not hasattr(marker_layer_ref.current, 'markers'):
                    print("Error: marker_layer_ref.current.markers not initialized.")
                    return

                marker_layer_ref.current.markers.clear()  # Clear existing markers
                new_markers = [] # List to hold newly created markers

                if isinstance(locations_data, dict) and 'data' in locations_data:
                    location_list = locations_data.get('data')
                    if isinstance(location_list, list):
                        for location in location_list:
                            if isinstance(location, dict):
                                latitude = location.get('latitude')
                                longitude = location.get('longitude')
                                shopname = (str(location.get('shopname', ''))).split(' ')[0]

                                if latitude is not None and longitude is not None:
                                    try:
                                        latitude = float(latitude)
                                        longitude = float(longitude)
                                        marker = map.Marker(
                                            content=ft.Stack(
                                                [
                                                    ft.Container(  # Container for text to control width and offset
                                                        ft.Text(shopname, style=ft.TextThemeStyle.BODY_SMALL, no_wrap=True),  # Shop name text, no wrap
                                                        alignment=ft.alignment.top_center,  # Align text to top center
                                                    ),
                                                    ft.Container(  # Container for icon to position below text
                                                        content=ft.Icon(ft.icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=25),  # Marker style, corrected CupertinoColors
                                                        alignment=ft.alignment.center,  # Align icon to bottom center
                                                    ),
                                                ],
                                            ),
                                            height=50,  # Adjust height as needed
                                            width=75,  # Adjust width as needed
                                            alignment=ft.alignment.top_center,  # Ensure marker aligns from top-center
                                            coordinates=map.MapLatitudeLongitude(latitude, longitude),  # Set marker coordinates
                                            data={'shopid': location.get('shopid'), 'shopname': location.get('shopname'), 'formattedaddress': location.get('formattedaddress'), 'shortdescription': location.get('shortdescription')}  # Store shop ID in marker data
                                        )
                                        new_markers.append(marker) # Append new marker to the list

                                    except (ValueError, TypeError) as e:
                                        print(f"Error: Invalid coords for shop {location.get('shopid')}: {e}")
                                else:
                                    print(f"Skipping shop {location.get('shopid')}: Missing lat/long for shop {location.get('shopid')}")
                            else:
                                print(f"Warning: Location data item is not a dictionary: {location}")
                    else:
                        print(f"Warning: locations_data['data'] is not a list as expected: {location_list}")

                else:
                    print(f"Warning: locations_data is not a dictionary with 'data' key, or not a dictionary at all: {locations_data}")

                marker_layer_ref.current.markers.extend(new_markers) # Extend the marker layer with the new markers
                self.page.session.set("marker_layer", marker_layer_ref.current.markers) # Store the marker layer in session
                self.page.session.set("db_state_hash", current_data_hash) # Update hash
                marker_layer_ref.current.update()

            else:
                print(f"Error fetching map locations: {response.status_code} - {response.text}")

        def handle_tap(e: map.MapTapEvent):
            coordinates = (e.coordinates.latitude, e.coordinates.longitude)

            for marker in marker_layer_ref.current.markers:
                marker_coords = (marker.coordinates.latitude, marker.coordinates.longitude)

                if is_within_radius(marker_coords, coordinates, radius=30):

                    for m in marker_layer_ref.current.markers:
                        m.content = ft.Stack(
                            [
                                ft.Container(  # Container for text to control width and offset
                                    ft.Text(m.data.get('shopname', 'New Marker'), style=ft.TextThemeStyle.BODY_SMALL, no_wrap=True),  # Shop name text, no wrap, default to 'New Marker' if no shopname
                                    alignment=ft.alignment.top_center,  # Align text to top center
                                ),
                                ft.Container(  # Container for icon to position below text
                                    content=ft.Icon(ft.icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=25),  # Marker style, corrected CupertinoColors
                                    alignment=ft.alignment.center,  # Align icon to bottom center
                                ),
                            ],
                        )
                    marker.content = ft.Icon(ft.icons.LOCATION_ON, color="blue", size=40)
                    marker_layer_ref.current.update()

                    cebu.center_on(map.MapLatitudeLongitude((marker.coordinates.latitude) * 0.999763, (marker.coordinates.longitude)), zoom=16.6)

                    self.open_bottom_sheet(e, marker.data)
                    return

            for marker_id, coord in self.marker_data.items():
                if is_within_radius(coord, coordinates, radius=30):
                    print(f"Too close to marker ID {marker_id}, cannot place here!")
                    return


        cebu = map.Map(
            expand=True,
            initial_zoom=14.5,
            initial_center=map.MapLatitudeLongitude(10.3055, 123.8938),
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL
            ),
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
                    markers=[], # Markers are now loaded dynamically
                ),
            ]
        )

        first_page_contents = ft.Container(
            margin=ft.margin.only(left=20),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Row(alignment='spaceBetween',
                        controls=[
                            ft.Container(on_click=self.shrink,
                                content=ft.Icon(ft.Icons.MENU, color=fg1,)
                            ),
                            self.search_bar,  # Expandable search bar
                        ]
                    ),
                    ft.Divider(height=7, color="transparent"),
                    ft.Container(
                        bgcolor=ft.colors.with_opacity(0.8, "#ececec"),
                        border_radius=ft.border_radius.only(top_left=18, top_right=18, bottom_left=18, bottom_right=18),
                        border=ft.border.all(0.5, "#b6b6b6"),
                        content=ft.Container(
                            margin=ft.margin.only(right=5, left=5, top=5, bottom=5),
                            border=ft.border.all(1, "#c9c9c9"),
                            width=320,  # Slightly bigger than map container
                            height=543,
                            border_radius=13,  # Ensures a rounded border
                            padding=1,  # Space for border thickness
                            content=ft.Container(
                                content=cebu,
                                width=580,
                                height=541,
                                border_radius=10,  # Ensures rounded corners inside
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Ensures map stays within rounded shape
                            )
                        )
                    )
                ]
            ),
            on_click=self.close_search,  # Detect clicks outside search bar
        )

        self.page_1 = ft.Container(
            bgcolor=bg,
            border_radius=0,
            padding=ft.padding.only(left=50, top=60, right=150),
            content=ft.Column(
                controls=[
                    circle,
                    ft.Divider(height=10, color="transparent"),
                    ft.Text(self.name, size=28, color=wg),
                    ft.Divider(height=15, color="transparent"),
                    ft.TextButton(
                        text="Favorites",
                        icon=ft.icons.FAVORITE_BORDER_SHARP,
                        on_click=lambda e: self.page.go("/favorite"),
                        style=ft.ButtonStyle(
                            color=wg,
                            icon_color=wg,
                            padding=ft.padding.all(10)
                        )
                    ),
                    ft.TextButton(
                        text="Assistant",
                        icon=ft.icons.AUTO_AWESOME_OUTLINED,
                        on_click=lambda e: self.page.go("/ai"),

                        style=ft.ButtonStyle(
                            color=wg,
                            icon_color=wg,
                            padding=ft.padding.all(10)
                        )
                    ),
                    ft.TextButton(
                        text="Create",
                        icon=ft.icons.ADD,
                        on_click=lambda e: self.page.go("/create"),
                        style=ft.ButtonStyle(
                            color=wg,
                            icon_color=wg,  # Change to your desired color
                            padding=ft.padding.all(10)
                        )
                    ),
                    ft.TextButton(
                        text="Preferences",
                        icon=ft.icons.SETTINGS,
                        on_click=lambda e: self.page.go("/preference"),
                        style=ft.ButtonStyle(
                            color=wg,
                            icon_color=wg,
                            padding=ft.padding.all(10)
                        )
                    ),
                    ft.TextButton(
                        text="About",
                        icon=ft.icons.INFO_OUTLINE_ROUNDED,
                        on_click=lambda e: self.page.go("/about"),
                        style=ft.ButtonStyle(
                            color=wg,
                            icon_color=wg,
                            padding=ft.padding.all(10)
                        )
                    ),

                    ft.Divider(height=20, color="transparent"),
                    ft.TextButton(
                        text="Sign Out",
                        icon=ft.icons.LOGOUT,
                        on_click=lambda e: self.page.go("/"),
                        style=ft.ButtonStyle(
                            color=wg,
                            icon_color=wg,
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
                    bgcolor=wg,
                    border_radius=0,
                    animate=ft.animation.Animation(600, ft.AnimationCurve.DECELERATE),
                    animate_scale=ft.animation.Animation(400, curve='decelerate'),
                    padding=ft.padding.only(
                        top=12, right=17, bottom=0,
                    ),
                    content=ft.Stack(
                        height=667,
                        controls=[
                            first_page_contents,
                            self.bottom_sheet,
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

    def open_bottom_sheet(self, e, marker_data):
        self.bottom_sheet.show(marker_data)  # Pass marker_data to the modified show method

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
        if self.is_shrunk:  # If already shrunk, restore
            self.restore(e)
            self.is_shrunk = False
        else:  # Shrink if not already shrunk
            self.page_2.controls[0].width = 150
            self.page_2.controls[0].scale = ft.transform.Scale(
                scale=0.8,
                alignment=ft.alignment.center_right
            )
            self.page_2.controls[0].border_radius = ft.border_radius.only(
                top_left=35,
                top_right=0,
                bottom_left=35,
                bottom_right=0
            )
            self.page_2.controls[0].padding = ft.padding.only(
                top=12,
                left=0,
                right=0,
                bottom=0,
            )
            self.close_search(e)
            self.search_bar.update()
            self.bottom_sheet.hide()
            self.page_2.update()
            self.is_shrunk = True  # Mark as shrunk

    def restore(self, e):
        self.page_2.controls[0].width = 375
        self.page_2.controls[0].scale = ft.transform.Scale(
            1, alignment=ft.alignment.center_right
        )
        self.page_2.controls[0].border_radius = ft.border_radius.only(
            top_left=0,
            top_right=0,
            bottom_left=0,
            bottom_right=0
        )
        self.page_2.controls[0].padding = ft.padding.only(
            top=12,
            right=17,
            bottom=0,
        )
        self.page_2.update()
        self.is_shrunk = False  # Mark as not shrunk

    def display_map_container(self):
        return ft.Container(
            expand=True,
            bgcolor='green',
            border_radius=0,
            content=ft.Stack(
                expand=True,
                controls=[
                    self.page_1,
                    self.page_2,
                ]
            )
        )
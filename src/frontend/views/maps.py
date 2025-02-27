import flet as ft
from components.description import BottomSheet
import flet.map as map
import math
import os
import requests


class Maps(ft.View):
    def __init__(self, page: ft.Page):
        name = 'Kint Louise Borbano'
        super(Maps, self).__init__(route="/maps")
        self.page = page
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
            padding=ft.padding.only(right=20),
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
            locations_api_url = os.getenv("LOCATIONS_API_URL") # API URL from environment
            response = requests.get(locations_api_url) # Fetch data from API

            if response.status_code == 200: # API call successful
                locations_data = response.json() # Parse JSON response
                print(f"Locations Data from API: {locations_data}") # Debug: print API data

                # --- Ensure marker_layer_ref is valid ---
                if marker_layer_ref.current is None: # Check if marker_layer_ref is initialized
                    print("Error: marker_layer_ref.current is None. Map init issue.")
                    return
                if not hasattr(marker_layer_ref.current, 'markers'): # Check if markers list exists
                    print("Error: marker_layer_ref.current.markers not initialized.")
                    return

                marker_layer_ref.current.markers.clear() # Clear existing markers on map

                for location in locations_data: # Loop through API locations
                    latitude = location.get('latitude') # Get latitude, handle missing key
                    longitude = location.get('longitude') # Get longitude, handle missing key

                    if latitude is not None and longitude is not None: # Check for valid coordinates
                        try:
                            latitude = float(latitude) # Convert latitude to float
                            longitude = float(longitude) # Convert longitude to float
                            marker = map.Marker( # Create a new map marker
                                content=ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED, size=25), # Marker style
                                coordinates=map.MapLatitudeLongitude(latitude, longitude), # Set marker coordinates
                                data={"shopid": location['shopid']} # Store shop ID in marker data
                            )
                            marker_layer_ref.current.markers.append(marker) # Add marker to marker layer

                        except (ValueError, TypeError) as e: # Handle coordinate conversion errors
                            print(f"Error: Invalid coords for shop {location.get('shopid')}: {e}")
                    else: # Skip location with missing coordinates
                        print(f"Skipping shop {location.get('shopid')}: Missing lat/long.")

                marker_layer_ref.current.update() # Update map to show markers
                print("Initial map markers loaded using marker_layer_ref.") # Confirmation msg

            else: # API call failed
                print(f"Error fetching map locations: {response.status_code} - {response.text}") # API error info

        def handle_tap(e: map.MapTapEvent):
            coordinates = (e.coordinates.latitude, e.coordinates.longitude)

            # Check if the tapped location is near an existing marker
            for marker in marker_layer_ref.current.markers:
                marker_coords = (marker.coordinates.latitude, marker.coordinates.longitude)
                
                if is_within_radius(marker_coords, coordinates, radius=30):  # Use radius for easier detection
                    
                    # Reset all markers to default size
                    for m in marker_layer_ref.current.markers:
                        m.content = ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED, size=25)

                    # Enlarge the selected marker
                    marker.content = ft.Icon(ft.icons.LOCATION_ON, color="blue", size=40)  
                    marker_layer_ref.current.update()

                    self.open_bottom_sheet(e)
                    return
            
            # # Prevent placing a new marker if it's too close to an existing one
            # for marker_id, coord in self.marker_data.items():
            #     if is_within_radius(coord, coordinates, radius=30):  
            #         print(f"Too close to marker ID {marker_id}, cannot place here!")
            #         return  

            # # Assign a unique ID and store the new marker
            # marker_id = self.marker_counter
            # self.marker_counter += 1
            # self.marker_data[marker_id] = coordinates

            # # Add new marker
            # marker_layer_ref.current.markers.append(
            #     map.Marker(
            #         content=ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED, size=25),
            #         coordinates=e.coordinates,
            #     )
            # )
            # marker_layer_ref.current.update()

            # print(f"Added marker ID: {marker_id} at {coordinates}")  


        cebu = map.Map(
            expand=True,
            initial_zoom=14.5,
            initial_center=map.MapLatitudeLongitude(10.3055, 123.8938), 
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL
            ),
            # on_init=lambda e: (print(f"Initialized Map"), get_initial_map_markers),
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
                    ft.Divider(height=10, color="transparent"),
                    ft.Container(
                    width=320,  # Slightly bigger than map container
                    height=543,
                    border_radius=21,  # Ensures a rounded border
                    bgcolor=ft.colors.BLACK,  # Border color
                    padding=1,  # Space for border thickness
                        content=ft.Container(
                        content=cebu,
                        width=580,
                        height=541,
                        border_radius=20,  # Ensures rounded corners inside
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,  # Ensures map stays within rounded shape     
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
                    ft.Text(name, size=28, weight='bold', color=wg),
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
                        top=12, left=20, right=17, bottom=0,
                    ),
                    content=ft.Stack(
                        controls=[
                            first_page_contents,
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
                left=22,
                right=0,
                bottom=10,
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
            left=22,
            right=17,
            bottom=10,
        )
        self.page_2.update()
        self.is_shrunk = False  # Mark as not shrunk

    def display_map_container(self):
        # self.get_initial_map_markers()
        return ft.Container(expand=True, bgcolor='green', border_radius=0, 
        content=ft.Stack(
            controls=[
                self.page_1,
                self.page_2,
            ]
        )
    )


import flet as ft
from components.prompt import Prompt
import flet.map as map
import math
from dotenv import load_dotenv
import os
import requests
from google import genai
from google.genai import types


def configure():
    load_dotenv()

class AI(ft.View):

    def __init__(self, page: ft.Page):
        super().__init__(route="/ai")
        self.client = self.create_client()
        self.page = page
        # Define color scheme (only those in use)
        wg = '#f8f9ff'
        fg1 = '#5f82a6'

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        self.marker_data = {}
        self.marker_counter = 1
        self.prompt_sheet = Prompt(self.close_prompt_sheet) 

        def on_bottom_button_click(e):
            response = self.get_best_store_recommendation()
            print(response)  # This will print the response in the console

        def on_preference_button_click(e):
            print("preference button clicked")  # Debugging
            self.page.go("/preference")

        def on_home_button_click(e):
            print("home button clicked")  # Debugging
            self.page.go("/maps")


        self.bottom_button = ft.Stack(
            alignment=ft.alignment.center,  # Ensures both containers are centered
            controls=[
                ft.Container(
                    width=75,  # Slightly bigger background
                    height=75,
                    bgcolor=ft.colors.with_opacity(0.8, "#ececec"),
                    border_radius=50,
                    border=ft.border.all(0.5, "#b6b6b6"),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=10,
                        color=ft.colors.BLACK38,
                        offset=ft.Offset(2, 4),
                    ),
                ),
                ft.Container(
                    width=60,
                    height=60,
                    bgcolor="#323232",
                    border_radius=50,
                    border=ft.border.all(3, "#c9c9c9"),
                    alignment=ft.alignment.center,  # Center alignment
                    content=ft.IconButton(
                        icon=ft.icons.SEARCH,
                        icon_size=25,
                        icon_color="white",
                        on_click=on_bottom_button_click
                    ),

                ),
            ]
        )

        self.home_button = ft.Stack(
            alignment=ft.alignment.center,  # Ensures both containers are centered
            controls=[
                ft.Container(
                    width=62,  # Slightly bigger background
                    height=62,
                    bgcolor=ft.colors.with_opacity(0.8, "#ececec"),
                    border_radius=50,
                    border=ft.border.all(0.5, "#b6b6b6"),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=10,
                        color=ft.colors.BLACK38,
                        offset=ft.Offset(2, 4),
                    ),
                ),
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor="#323232",
                    border_radius=50,
                    border=ft.border.all(2, "#b6b6b6"),
                    alignment=ft.alignment.center,  # Center alignment
                    content=ft.IconButton(
                        icon=ft.icons.HOME,
                        icon_size=19,
                        icon_color="white",
                        on_click=on_home_button_click
                    ),

                ),
            ]
        )
        
        self.preferences_button = ft.Stack(
            alignment=ft.alignment.center,  # Ensures both containers are centered
            controls=[
                ft.Container(
                    width=62,  # Slightly bigger background
                    height=62,
                    bgcolor=ft.colors.with_opacity(0.8, "#ececec"),
                    border_radius=50,
                    border=ft.border.all(0.5, "#b6b6b6"),
                    shadow=ft.BoxShadow(
                        spread_radius=2,
                        blur_radius=10,
                        color=ft.colors.BLACK38,
                        offset=ft.Offset(2, 4),
                    ),
                ),
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor="#323232",
                    border_radius=50,
                    border=ft.border.all(2, "#b6b6b6"),
                    alignment=ft.alignment.center,  # Center alignment
                    content=ft.IconButton(
                        icon=ft.icons.SETTINGS,
                        icon_size=19,
                        icon_color="white",
                        on_click=on_preference_button_click
                    ),

                ),
            ]
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
                                        ft.Container(
                                        left=143,
                                        top=500,
                                        content=self.bottom_button,  # Wrap in a list
                                        ),
                                        ft.Container(
                                            left=58,
                                            top=506,
                                            content=self.home_button,  # Wrap in a list
                                        ),
                                        ft.Container(
                                            left=240,
                                            top=506,
                                            content=self.preferences_button,  # Wrap in a list
                                        ),
                                         self.prompt_sheet])
                )
            ]
        )
        self.initialize()

    def create_client(self):
        return genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

    def fetch_reviews(self):
        """Fetch store reviews from an API"""
        try:
            store_api_url = os.getenv("THRIFTSTORE_API_URL")  # API endpoint
            response = requests.get(store_api_url)

            if response.status_code == 200:
                data = response.json()  # Convert JSON response to Python object
                print("Fetched store reviews:", data)  # Debugging output
                return data
            else:
                print("Failed to fetch store reviews:", response.status_code, response.text)
                return None
                
        except Exception as e:
            print("Error fetching data:", e)
            return None

    def format_store_reviews_for_llm(self, stores_data):
        """Format store reviews for LLM input"""
        if not stores_data:
            return "No store reviews available."

        formatted_review = "Here are the available stores and their reviews:\n\n"
        for entry in stores_data:
            shop_name = entry.get("ShopName", "Unknown Store")
            review = entry.get("Review", "No review available")
            formatted_review += f"- {shop_name}: {review}\n"

        print("Formatted store reviews:", formatted_review)  # Debugging output
        return formatted_review

    def fetch_preference(self):
        """Fetch user preferences from an API"""
        try:
            preference_api_url = os.getenv("USERS_PREF_API_URL")  # API endpoint
            response = requests.get(preference_api_url)
            if response.status_code == 200:
                data = response.json()  # Convert JSON response to Python object
                print("Fetched user preferences:", data)  # Debugging output
                return data
            else:
                print("Failed to fetch user preference:", response.status_code, response.text)
                return None
                
        except Exception as e:
            print("Error fetching data:", e)
            return None

    def format_user_preference_for_llm(self, preference_data):
        """Format user preference for LLM input"""
        if not preference_data:
            return "No user preference available."

        formatted_preference = "Here are the available user preferences:\n\n"
        for entry in preference_data:
            clothing = entry.get("clothing", "N/A")
            shoppingenvironment = entry.get("shoppingenvironment", "N/A")
            budget = entry.get("budget", "N/A")
            organization = entry.get("organization", "N/A")
            interest = entry.get("interest", "N/A")
            username = entry.get("username", "N/A")
            formatted_preference += (
                f"- {username}: likes {clothing} and hopes to shop in {shoppingenvironment} "
                f"with a {budget} and a setting that can be described as {organization}. "
                f"Lastly, the user is interested in {interest}.\n"
            )

        print("Formatted user preferences:", formatted_preference)  # Debugging output
        return formatted_preference
    def get_best_store_recommendation(self):
        """Get the best store recommendation based on user preference"""
        stores_data = self.fetch_reviews()
        preference_data = self.fetch_preference()

        formatted_review = self.format_store_reviews_for_llm(stores_data)
        formatted_preference = self.format_user_preference_for_llm(preference_data)

        max_length = 500

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"Out of the {formatted_review}, determine the store that best fits the preference of user {formatted_preference} (max {max_length} chars). Pick only one store:\n\n"
            ],
        )

        return response


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

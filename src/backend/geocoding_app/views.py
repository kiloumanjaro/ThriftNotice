from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .geocoding import get_geocode

@csrf_exempt
def geocode_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address = data.get("address", "Enter an address")  # Placeholder default value

            if address == "Enter an address":
                return JsonResponse({"error": "Address is required", "placeholder": address}, status=400)

            result = get_geocode(address)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

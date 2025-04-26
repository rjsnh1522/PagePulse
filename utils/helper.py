import requests
import bcrypt


def find_country_by_ip(ip):
    try:
        # First try ipapi.co
        response = requests.get(f"https://ipapi.co/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            # Already separate latitude and longitude
            return {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                **data
            }

        # If rate limited, fallback to ipinfo.io
        elif response.status_code == 429:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            if response.status_code == 200:
                data = response.json()
                loc = data.get("loc")  # Example: "37.3860,-122.0840"
                latitude, longitude = (None, None)
                if loc:
                    latitude, longitude = map(float, loc.split(","))
                return {
                    "latitude": latitude,
                    "longitude": longitude,
                    **data
                }

    except Exception as e:
        print(f"IP lookup failed: {e}")

    return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
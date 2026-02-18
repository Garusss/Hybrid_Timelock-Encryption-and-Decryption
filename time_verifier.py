import requests
from datetime import datetime

def get_trusted_time():
    try:
        response = requests.get(
            "https://timeapi.io/api/v1/time/current/utc",
            timeout=5
        )

        data = response.json()
        iso_time = data["utc_time"]

        iso_time = iso_time.replace("Z", "+00:00")

        if "." in iso_time:
            date_part, frac_part = iso_time.split(".")
            if "+" in frac_part:
                micro, tz = frac_part.split("+")
                micro = micro[:6]
                iso_time = f"{date_part}.{micro}+{tz}"

        return datetime.fromisoformat(iso_time)

    except Exception as e:
        print("Time verification error:", e)
        return None

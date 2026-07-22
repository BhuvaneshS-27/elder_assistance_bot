import requests
from datetime import datetime, timedelta
from config import WEATHER_LATITUDE, WEATHER_LONGITUDE

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# How long a successful fetch stays valid before re-hitting the API.
# Purely a performance/politeness cache — NOT used to paper over a
# failed live fetch. If a live call fails, get_weather() returns None
# and the caller tells the user honestly, rather than silently serving
# old data as if it were current.
CACHE_FRESHNESS = timedelta(minutes=30)

_cache = {
    "data": None,
    "fetched_at": None,
}

# WMO weather codes, as used by Open-Meteo's `weathercode` field
WEATHER_CODES = {
    0: "clear sky",
    1: "mostly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy with frost",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    80: "light rain showers",
    81: "rain showers",
    82: "heavy rain showers",
    95: "thunderstorms",
    96: "thunderstorms with hail",
    99: "severe thunderstorms with hail",
}


def describe_code(code):
    return WEATHER_CODES.get(code, "unclear conditions")


def _fetch_live():
    params = {
        "latitude": WEATHER_LATITUDE,
        "longitude": WEATHER_LONGITUDE,
        "current": "temperature_2m,precipitation,weathercode",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "temperature_unit": "celsius",
    }

    # Short timeout — a dead/slow connection shouldn't stall an
    # otherwise-fast voice turn for a long time.
    response = requests.get(WEATHER_URL, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})

    return {
        "current_temp": current.get("temperature_2m"),
        "current_code": current.get("weathercode"),
        "today_high": (daily.get("temperature_2m_max") or [None])[0],
        "today_low": (daily.get("temperature_2m_min") or [None])[0],
        "rain_chance": (daily.get("precipitation_probability_max") or [None])[0],
    }


def get_weather():
    """
    Returns a weather dict, or None if a live fetch failed and there's
    no cache to fall back on — the caller is responsible for telling
    the user honestly that weather isn't available right now.
    """
    now = datetime.now()

    if _cache["data"] is not None and _cache["fetched_at"] is not None:
        if now - _cache["fetched_at"] < CACHE_FRESHNESS:
            return _cache["data"]

    try:
        data = _fetch_live()
        _cache["data"] = data
        _cache["fetched_at"] = now
        return data
    except Exception as e:
        print("Weather fetch error:", e)
        return None
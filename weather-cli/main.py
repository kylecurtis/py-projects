# =============================================================================
# IMPORTS
# =============================================================================
import argparse
import os
import sys
from datetime import datetime

import colorama
import requests
from colorama import Fore, Style

# Add root directory to path for importing utils
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)


from utils.env_utils import get_api_key  # noqa: E402

# =============================================================================
# COLORAMA SETUP
# =============================================================================
# Initialize colorama for cross-platform colored terminal text
colorama.init(autoreset=True)

# ANSI color codes
COLORS = {
    "RED": Fore.RED,
    "GREEN": Fore.GREEN,
    "YELLOW": Fore.YELLOW,
    "BLUE": Fore.BLUE,
    "MAGENTA": Fore.MAGENTA,
    "CYAN": Fore.CYAN,
    "WHITE": Fore.WHITE,
    "RESET": Style.RESET_ALL,
    "BOLD": Style.BRIGHT,
}

WEATHER_COLORS = {
    "sunny": Fore.YELLOW,
    "cloudy": Fore.WHITE,
    "rainy": Fore.CYAN,
    "snowy": Fore.WHITE,
    "thunder": Fore.MAGENTA,
    "clear_night": Fore.WHITE,
}

# =============================================================================
# WEATHER CONDITION ICONS (UNICODE)
# =============================================================================
WEATHER_ICONS = {
    # Clear conditions
    1000: "\u2600\ufe0f ",  # Sunny / Clear
    1003: "\U0001f324\ufe0f ",  # Partly cloudy
    1006: "\u26c5 ",  # Cloudy
    1009: "\u2601\ufe0f ",  # Overcast
    # Precipitation
    1030: "\U0001f32b\ufe0f ",  # Mist
    1063: "\U0001f326\ufe0f ",  # Patchy rain
    1066: "\U0001f328\ufe0f ",  # Patchy snow
    1069: "\U0001f327\ufe0f ",  # Patchy sleet
    1072: "\U0001f327\ufe0f ",  # Patchy freezing drizzle
    1087: "\u26c8\ufe0f ",  # Thundery outbreaks
    1114: "\u2744\ufe0f ",  # Blowing snow
    1117: "\U0001f328\ufe0f ",  # Blizzard
    1135: "\U0001f32b\ufe0f ",  # Fog
    1147: "\U0001f32b\ufe0f ",  # Freezing fog
    # Rain
    1150: "\U0001f327\ufe0f ",  # Patchy light drizzle
    1153: "\U0001f327\ufe0f ",  # Light drizzle
    1168: "\U0001f327\ufe0f ",  # Freezing drizzle
    1171: "\U0001f327\ufe0f ",  # Heavy freezing drizzle
    1180: "\U0001f327\ufe0f ",  # Patchy light rain
    1183: "\U0001f327\ufe0f ",  # Light rain
    1186: "\U0001f327\ufe0f ",  # Moderate rain at times
    1189: "\U0001f327\ufe0f ",  # Moderate rain
    1192: "\U0001f327\ufe0f ",  # Heavy rain at times
    1195: "\U0001f327\ufe0f ",  # Heavy rain
    1198: "\U0001f327\ufe0f ",  # Light freezing rain
    1201: "\U0001f327\ufe0f ",  # Moderate or heavy freezing rain
    # Snow
    1204: "\U0001f328\ufe0f ",  # Light sleet
    1207: "\U0001f328\ufe0f ",  # Moderate or heavy sleet
    1210: "\U0001f328\ufe0f ",  # Patchy light snow
    1213: "\U0001f328\ufe0f ",  # Light snow
    1216: "\U0001f328\ufe0f ",  # Patchy moderate snow
    1219: "\U0001f328\ufe0f ",  # Moderate snow
    1222: "\U0001f328\ufe0f ",  # Patchy heavy snow
    1225: "\u2744\ufe0f ",  # Heavy snow
    1237: "\u2744\ufe0f ",  # Ice pellets
    # Rain variations
    1240: "\U0001f327\ufe0f ",  # Light rain shower
    1243: "\U0001f327\ufe0f ",  # Moderate or heavy rain shower
    1246: "\U0001f327\ufe0f ",  # Torrential rain shower
    1249: "\U0001f327\ufe0f ",  # Light sleet showers
    1252: "\U0001f327\ufe0f ",  # Moderate or heavy sleet showers
    # Snow variations
    1255: "\U0001f328\ufe0f ",  # Light snow showers
    1258: "\U0001f328\ufe0f ",  # Moderate or heavy snow showers
    1261: "\u2744\ufe0f ",  # Light showers of ice pellets
    1264: "\u2744\ufe0f ",  # Moderate or heavy showers of ice pellets
    # Thunderstorms
    1273: "\u26c8\ufe0f ",  # Patchy light rain with thunder
    1276: "\u26c8\ufe0f ",  # Moderate or heavy rain with thunder
    1279: "\u26c8\ufe0f ",  # Patchy light snow with thunder
    1282: "\u26c8\ufe0f ",  # ️Moderate or heavy snow with thunder
}

# Moon icons for different phases
MOON_ICONS = {
    "New Moon": "\U0001f311 ",  # New Moon
    "Waxing Crescent": "\U0001f312 ",  # Waxing Crescent
    "First Quarter": "\U0001f313 ",  # First Quarter
    "Waxing Gibbous": "\U0001f314 ",  # Waxing Gibbous
    "Full Moon": "\U0001f315 ",  # Full Moon
    "Waning Gibbous": "\U0001f316 ",  # Waning Gibbous
    "Last Quarter": "\U0001f317 ",  # Last Quarter
    "Waning Crescent": "\U0001f318 ",  # Waning Crescent
}

# =============================================================================
# WEATHER ASCII ART LOGOS
# =============================================================================
WEATHER_LOGO = {
    "sunny": [
        "    \\   /   ",
        "     .-.     ",
        "  ― (   ) ― ",
        "     `-'     ",
        "    /   \\   ",
    ],
    "cloudy": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "             ",
    ],
    "rainy": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "    , , , ,  ",
        "    , , , ,  ",
    ],
    "snowy": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "    * * * *  ",
        "    * * * *  ",
    ],
    "thunder": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "    ⚡︎  ⚡︎  ⚡︎  ",
        "   ⚡︎  ⚡︎  ⚡︎   ",
    ],
}

# Add basic night logo for when we don't have moon phase or as fallback
NIGHT_LOGO = {"clear_night": []}

# Detailed moon phase ASCII art
MOON_PHASE_ASCII = {
    "New Moon": [
        "     _..._   ",
        "   .:::::::. ",
        "  :::::::::::",
        "  :::::::::::",
        "  `:::::::::'",
        "    `':::''  ",
    ],
    "Waxing Crescent": [
        "     _..._   ",
        "   .::::. `. ",
        "  :::::::.  :",
        "  ::::::::  :",
        "  `::::::' .'",
        "    `'::'-'  ",
    ],
    "First Quarter": [
        "     _..._   ",
        "   .::::  `. ",
        "  ::::::    :",
        "  ::::::    :",
        "  `:::::   .'",
        "    `'::.-'  ",
    ],
    "Waxing Gibbous": [
        "     _..._   ",
        "   .::'   `. ",
        "  :::       :",
        "  :::       :",
        "  `::.     .'",
        "    `':..-'  ",
    ],
    "Full Moon": [
        "     _..._   ",
        "   .'     `. ",
        "  :         :",
        "  :         :",
        "  `.       .'",
        "    `-...-'  ",
    ],
    "Waning Gibbous": [
        "     _..._   ",
        "   .'   `::. ",
        "  :       :::",
        "  :       :::",
        "  `.     .::'",
        "    `-..:''  ",
    ],
    "Last Quarter": [
        "     _..._   ",
        "   .'  ::::. ",
        "  :    ::::::",
        "  :    ::::::",
        "  `.   :::::'",
        "    `-.::''  ",
    ],
    "Waning Crescent": [
        "     _..._   ",
        "   .' .::::. ",
        "  :  ::::::::",
        "  :  ::::::::",
        "  `. '::::::'",
        "    `-.::''  ",
    ],
}


# =============================================================================
# GET CONDITION LOGO
# Function to map API weather codes to ASCII art categories
# =============================================================================
def get_logo_for_condition_code(code, is_day=True):
    if code == 1000:  # Clear/Sunny
        if is_day:
            return "sunny"  # Daytime clear -> sun
        else:
            return "clear_night"  # Nighttime clear -> moon
    elif code in [1003, 1006, 1009, 1030, 1135, 1147]:  # Cloudy conditions
        return "cloudy"
    elif code in [1273, 1276, 1279, 1282]:  # Thunderstorms
        return "thunder"
    elif code in [
        1210,
        1213,
        1216,
        1219,
        1222,
        1225,
        1237,
        1255,
        1258,
        1261,
        1264,
    ]:  # Snow
        return "snowy"
    else:  # Default to rainy for all other precipitation
        return "rainy"


# =============================================================================
# GET WEATHER ICON (FOR MOON)
# =============================================================================
def get_weather_icon(weather_code, is_daytime, moon_phase=""):
    # At night, always use the moon phase for any weather condition
    if not is_daytime and moon_phase:
        return MOON_ICONS.get(moon_phase, "\U0001f315 ")  # Default to full moon

    # During day or if no moon phase available, use standard weather icon
    return WEATHER_ICONS.get(
        weather_code, "\U0001f321\ufe0f "
    )  # Default to thermometer


# =============================================================================
# GET WEATHER DATA
# Function to fetch data from the weather API
# =============================================================================
def get_weather(api_key, location):
    # Current weather request
    weather_url = (
        f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes"
    )

    # Today's date for astronomy endpoint
    today = datetime.now().strftime("%Y-%m-%d")

    # Astronomy request (for sunrise, sunset, moon phase)
    astronomy_url = f"https://api.weatherapi.com/v1/astronomy.json?key={api_key}&q={location}&dt={today}"

    try:
        # Fetch current weather
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Fetch astronomy data
        astronomy_response = requests.get(astronomy_url)
        astronomy_response.raise_for_status()
        astronomy_data = astronomy_response.json()

        # Combine both datasets
        combined_data = weather_data.copy()
        combined_data["astronomy"] = astronomy_data.get("astronomy", {})

        return combined_data
    except Exception as e:
        print(f"{COLORS['RED']}Error fetching weather data: {e}")
        sys.exit(1)


# =============================================================================
# FORMAT TIME
# Function to convert API timestamp to a more readable format
# =============================================================================
def format_time(timestamp, format_str="%Y-%m-%d %H:%M"):
    try:
        # Parse the timestamp string into a datetime object
        dt = datetime.strptime(timestamp, format_str)
        # Format datetime into a more readable string
        return dt.strftime("%A, %B %d, %Y at %I:%M %p")
    except Exception:
        # Return the original timestamp if parsing fails
        return timestamp


# =============================================================================
# GET WIND DIRECTION ARROWS
# Function to convert degrees to directional arrow
# =============================================================================
def get_wind_direction_arrow(degrees):
    # Define the wind direction arrows (8 directions)
    arrows = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]

    # Convert degrees to one of 8 directions (divide by 45 degrees)
    index = round(degrees / 45) % 8
    return arrows[index]


# =============================================================================
# DAYTIME CHECK
# Function to check if it's daytime based on astronomy data
# =============================================================================
def is_daytime(data):
    if "astronomy" in data and "astro" in data["astronomy"]:
        astro = data["astronomy"]["astro"]
        if "is_sun_up" in astro:
            return astro["is_sun_up"] == 1

    # Fallback to checking the current hour against general sunrise/sunset times
    current_hour = datetime.now().hour
    return 6 <= current_hour < 18  # Assume daytime is 6 AM to 6 PM if no data


# =============================================================================
# UV INFORMATION
# Function to get description of UV index levels
# =============================================================================
def get_uv_description(uv_index):
    if uv_index <= 2:
        return f"{COLORS['GREEN']}Low"  # Low risk
    elif uv_index <= 5:
        return f"{COLORS['YELLOW']}Moderate"  # Moderate risk
    elif uv_index <= 7:
        return f"{COLORS['YELLOW']}High"  # High risk
    elif uv_index <= 10:
        return f"{COLORS['RED']}Very High"  # Very high risk
    else:
        return f"{COLORS['RED']}Extreme"  # Extreme risk


# =============================================================================
# AIR QUALITY INFORMATION
# Function to get description of air quality index
# =============================================================================
def get_air_quality_description(aqi):
    descriptions = [
        f"{COLORS['GREEN']}Good",  # Level 1
        f"{COLORS['YELLOW']}Moderate",  # Level 2
        f"{COLORS['YELLOW']}Unhealthy for Sensitive Groups",  # Level 3
        f"{COLORS['RED']}Unhealthy",  # Level 4
        f"{COLORS['RED']}Very Unhealthy",  # Level 5
        f"{COLORS['RED']}Hazardous",  # Level 6
    ]

    if 1 <= aqi <= 6:
        return descriptions[aqi - 1]
    return "Unknown"  # For values outside 1-6 range


# =============================================================================
# WEATHER DISPLAY
# Function to format and display the weather data to terminal
# =============================================================================
def display_weather(data, use_fahrenheit=True):
    # Extract main data components
    location = data["location"]
    current = data["current"]
    condition = current["condition"]

    # Get astronomy data if available
    astro = {}
    moon_phase = ""
    if "astronomy" in data and "astro" in data["astronomy"]:
        astro = data["astronomy"]["astro"]
        moon_phase = astro.get("moon_phase", "")

    # Check if it's daytime
    daytime = is_daytime(data)

    # Get temperature based on user preference
    temp = current["temp_f"] if use_fahrenheit else current["temp_c"]
    feels_like = current["feelslike_f"] if use_fahrenheit else current["feelslike_c"]
    temp_unit = "°F" if use_fahrenheit else "°C"

    # Get wind speed based on user preference
    wind_speed = current["wind_mph"] if use_fahrenheit else current["wind_kph"]
    speed_unit = "mph" if use_fahrenheit else "kph"

    # Get appropriate weather icon - use moon icon for clear night
    weather_code = condition["code"]
    weather_icon = get_weather_icon(weather_code, daytime, moon_phase)

    # Override with moon icon if it's clear at night
    if weather_code == 1000 and not daytime and moon_phase:
        weather_icon = MOON_ICONS.get(moon_phase, "\U0001f315 ")  # Default to full moon

    # Get ASCII art logo and its color
    logo_type = get_logo_for_condition_code(weather_code, daytime)

    # Select logo based on weather condition and time of day
    if logo_type == "clear_night" and moon_phase in MOON_PHASE_ASCII:
        # Use specific moon phase ASCII art for clear nights
        logo = MOON_PHASE_ASCII[moon_phase]
        logo_color = COLORS.get("BLUE", Fore.BLUE)  # Use blue for night sky
    elif logo_type == "clear_night":
        # Fallback to generic night sky if moon phase not found
        logo = NIGHT_LOGO["clear_night"]
        logo_color = COLORS.get("BLUE", Fore.BLUE)
    else:
        # Use regular weather ASCII art for other conditions
        logo = WEATHER_LOGO[logo_type]
        logo_color = WEATHER_COLORS.get(logo_type, Fore.WHITE)

    # Apply color to the logo
    colored_logo = [f"{logo_color}{line}{COLORS['RESET']}" for line in logo]

    # Format location and time information
    location_str = f"{location['name']}, {location['region']}, {location['country']}"
    local_time = format_time(current["last_updated"])

    # Format wind direction arrow
    wind_arrow = get_wind_direction_arrow(current["wind_degree"])

    # Format UV index description
    uv_desc = get_uv_description(current["uv"])

    # Air quality if available
    aqi_info = ""
    if "air_quality" in current and "us-epa-index" in current["air_quality"]:
        aqi = current["air_quality"]["us-epa-index"]
        aqi_desc = get_air_quality_description(aqi)
        aqi_info = (
            f"  {COLORS['BOLD']}Air Quality:{COLORS['RESET']} {aqi_desc} ({aqi}/6)"
        )

    moon_info = ""
    if moon_phase and not daytime:
        moon_info = f"\n{COLORS['BOLD']}Moon Phase:{COLORS['RESET']} {moon_phase}"

    # Build the output display
    # Left side - Logo (colored ASCII art)
    left_content = colored_logo

    # Determine padding based on logo type
    pad_width = (
        15 if logo_type == "clear_night" and moon_phase in MOON_PHASE_ASCII else 15
    )
    # Pad to match the longest line (accounting for ANSI color codes)
    left_content = [
        line.ljust(pad_width + len(logo_color) + len(COLORS["RESET"]))
        for line in left_content
    ]

    # Right side - Weather information
    right_template = [
        f"{COLORS['BOLD']}{COLORS['CYAN']}{location_str}{COLORS['RESET']}",  # Location
        f"{COLORS['BOLD']}Weather:{COLORS['RESET']} {weather_icon} {condition['text']}",  # Condition
        f"{COLORS['BOLD']}Temperature:{COLORS['RESET']} {temp}{temp_unit} (Feels like: {feels_like}{temp_unit})",  # Temp
        f"{COLORS['BOLD']}Humidity:{COLORS['RESET']} {current['humidity']}%",  # Humidity
        f"{COLORS['BOLD']}Wind:{COLORS['RESET']} {wind_speed} {speed_unit} {wind_arrow} {current['wind_dir']}",  # Wind
        f"{COLORS['BOLD']}Pressure:{COLORS['RESET']} {current['pressure_mb']} mb",  # Pressure
        f"{COLORS['BOLD']}Visibility:{COLORS['RESET']} {current['vis_miles']} miles",  # Visibility
        f"{COLORS['BOLD']}UV Index:{COLORS['RESET']} {current['uv']} ({uv_desc}{COLORS['RESET']})"
        + aqi_info,  # UV Index & AQI
    ]

    # Add moon phase info if available and it's night
    if moon_phase and not daytime:
        right_template.append(
            f"{COLORS['BOLD']}Moon Phase:{COLORS['RESET']} {moon_phase}"
        )

    # Add last updated time at the end
    right_template.append(f"{COLORS['BOLD']}Updated:{COLORS['RESET']} {local_time}")

    # Combine left and right content
    lines = []
    for i in range(max(len(left_content), len(right_template))):
        # Get left side content or empty space if we've run out of logo lines
        left = left_content[i] if i < len(left_content) else " " * pad_width
        # Get right side content or empty string if we've run out of template lines
        right = right_template[i] if i < len(right_template) else ""
        # Combine the two sides
        lines.append(f"{left} {right}")

    # Determine the length of the separator line based on the logo type
    separator_length = (
        72 if logo_type == "clear_night" and moon_phase in MOON_PHASE_ASCII else 64
    )
    # Add a separator line at the top and bottom
    separator = f"{COLORS['BLUE']}{'─' * separator_length}{COLORS['RESET']}"

    # Display the full output
    print(separator)  # Top separator
    for line in lines:  # Content lines
        print(line)
    print(separator)  # Bottom separator


# =============================================================================
# MAIN - Entry point of the program
# =============================================================================
def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Weather CLI - Display weather information in a terminal"
    )
    parser.add_argument("location", help="Location (city name, ZIP code, coordinates)")
    parser.add_argument(
        "--celsius",
        "-c",
        action="store_true",
        help="Display temperature in Celsius",
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Get API key from the .env file
    api_key = get_api_key("WEATHER_API_KEY", "./.env")

    # Check if API key was found
    if not api_key:
        print(
            f"{COLORS['RED']}Error: API key is required. Provide it with --api-key or set WEATHER_API_KEY environment variable."
        )
        sys.exit(1)  # Exit with error code

    # Get weather data for requested location
    data = get_weather(api_key, args.location)

    # Display weather information
    # Note: --celsius flag inverts the use_fahrenheit parameter
    display_weather(data, use_fahrenheit=not args.celsius)


# If this script is run directly (not imported)
if __name__ == "__main__":
    try:
        main()  # Run the main function
    except KeyboardInterrupt:
        print("\nExiting...")  # Handle ctrl+c gracefully
        sys.exit(0)  # Exit with success code

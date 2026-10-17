
"""Command-line weather tool. Run: python week08/weather.py --help"""

import argparse
import importlib.util
import os
from pathlib import Path
import sys

try:
    from .favorites import FavoritesManager
    from .weather_api import WeatherAPI, format_current_weather, format_forecast
except ImportError:
    from favorites import FavoritesManager
    from weather_api import WeatherAPI, format_current_weather, format_forecast


HERE = Path(__file__).resolve().parent
FAVORITES_FILE = HERE / "favorites.json"


def load_api_key():
    """Use the environment variable first, then local config.py."""
    key = os.environ.get("WEATHER_API_KEY")
    if key and key.strip():
        return key.strip()

    config_path = HERE / "config.py"
    if not config_path.is_file():
        return None

    try:
        spec = importlib.util.spec_from_file_location(
            "week08_local_config", config_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        key = getattr(module, "WEATHER_API_KEY", None)
        if key is None:
            key = getattr(module, "API_KEY", None)

        return key.strip() if isinstance(key, str) and key.strip() else None

    except (OSError, ImportError, SyntaxError):
        return None


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check weather and manage favorite locations."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    current = commands.add_parser("current", help="Show current weather")
    current.add_argument("location")

    forecast = commands.add_parser("forecast", help="Show weather forecast")
    forecast.add_argument("location")
    forecast.add_argument("--days", type=int, choices=range(1, 4), default=3)

    favorites = commands.add_parser(
        "favorites", help="Manage saved locations"
    )
    favorite_actions = favorites.add_subparsers(
        dest="favorites_command", required=True
    )

    add = favorite_actions.add_parser("add")
    add.add_argument("name")
    add.add_argument("location")

    favorite_actions.add_parser("list")

    remove = favorite_actions.add_parser("remove")
    remove.add_argument("name")

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    manager = FavoritesManager(FAVORITES_FILE)

    if args.command == "favorites":
        if args.favorites_command == "add":
            if not manager.add(args.name, args.location):
                print(
                    f"Favorite already exists: {args.name}",
                    file=sys.stderr
                )
                return 1
            print(f"Added favorite: {args.name} -> {args.location}")

        elif args.favorites_command == "remove":
            if not manager.remove(args.name):
                print(
                    f"Favorite not found: {args.name}",
                    file=sys.stderr
                )
                return 1
            print(f"Removed favorite: {args.name}")

        else:
            for name, location in manager.list_all().items():
                print(f"{name}: {location}")

        return 0

    key = load_api_key()

    if not key:
        print(
            "Missing API key. Set WEATHER_API_KEY or configure week08/config.py.",
            file=sys.stderr
        )
        return 1

    location = manager.get_location(args.location) or args.location
    api = WeatherAPI(key)

    if args.command == "current":
        data = api.get_current_weather(location)
        formatter = format_current_weather
    else:
        data = api.get_forecast(location, days=args.days)
        formatter = format_forecast

    if data is None:
        print(
            f"Weather request failed for {location}.",
            file=sys.stderr
        )
        return 1

    try:
        print(formatter(data))
    except (KeyError, TypeError, IndexError, ValueError) as exc:
        print(
            f"Invalid weather response: {exc}",
            file=sys.stderr
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

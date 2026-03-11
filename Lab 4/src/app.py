import os
import platform
import socket
from datetime import datetime, timezone


def main() -> None:
    app_name = os.getenv("APP_NAME", "Docker Lab 1 - Custom")
    city = os.getenv("CITY", "Boston")
    greeting = os.getenv("GREETING", "Hello")
    show_details = os.getenv("SHOW_DETAILS", "true").lower() in {"1", "true", "yes"}
    timestamp = datetime.now(timezone.utc).isoformat()

    print("Greeting:", greeting)
    print("App:", app_name)
    print("City:", city)
    print("UTC Time:", timestamp)
    print("Hostname:", socket.gethostname())
    print("User:", os.getenv("USER", "unknown"))

    if show_details:
        print("Python:", platform.python_version())
        print("Platform:", platform.platform())
    else:
        print("Python:", "hidden")
        print("Platform:", "hidden")


if __name__ == "__main__":
    main()

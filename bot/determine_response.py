"""Bot response handler"""


def determine_response(command: str) -> str:
    """Determines the response based on the input command"""

    match command:
        case "help":
            return "Sorry, nothing yet"
        case "play":
            return "Sorry, nothing yet"
        case "add to queue":
            return "Sorry, nothing yet"
        case _:
            return "What the fuck do you want?!"

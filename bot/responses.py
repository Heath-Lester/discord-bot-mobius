"""Bot response handler"""


def handle_response(command: str) -> str:
    """Determines the response based on the input command"""

    match command:
        case "help":
            return ""
        case _:
            return "What the fuck do you want?!"

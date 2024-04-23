"""Discord Message Utility Functions"""


def extract_ats_from_message_content(message_content: str, message_limit: int = 10000) -> list[str] | None:
    """Extracts @ mentions from message content"""
    message_length = len(message_content)

    if message_content is None or message_length == 0 or message_length > message_limit:
        return None

    ats_list: list[str] = []
    current_at = ""
    brackets_and_positions: dict = {}
    for i in range(message_length):
        character = message_content[i]

        if character == "<":
            if brackets_and_positions.get("<") is None and brackets_and_positions.get("@") is None:
                brackets_and_positions[character] = i
            else:
                brackets_and_positions.clear()
        elif character == "@":
            if brackets_and_positions.get("<") == i - 1 and brackets_and_positions.get("@") is None:
                brackets_and_positions[character] = i
            else:
                brackets_and_positions.clear()
        elif character == ">":
            if brackets_and_positions.get("<") is not None and brackets_and_positions.get("@") is not None and len(current_at) > 0:
                ats_list.append(current_at)
            current_at = ""
            brackets_and_positions.clear()
        elif brackets_and_positions.get("<") is not None and brackets_and_positions.get("@") is not None:
            current_at += character

    return ats_list


def does_ats_list_contain_id(ats_list: list[str] | None, target_id: str) -> bool:
    """Determines if id is contained in a list of ids"""
    if target_id is None or ats_list is None or len(ats_list) == 0:
        return False
    return target_id in ats_list


def does_message_mention_user(message_content: str, target_user_id: str | int) -> bool:
    """Determines if a message contains an @ mention for an id"""
    if message_content is None:
        print("Failed to determine if message mentions target user: Message is None")
        return False
    if target_user_id is None:
        print("Failed to determine if message mentions target user: User ID is None")
        return False
    if len(message_content) == 0:
        print("Failed to determine if message mentions target user: Message is empty")
        return False
    if message_content.isspace():
        print("Failed to determine if message mentions target user: Message is blank")
        return False

    if isinstance(target_user_id, int):
        target_user_id = str(target_user_id)

    if target_user_id.isspace():
        print(
            "Failed to determine if message mentions target user: Provided user ID is blank")
        return False

    return does_ats_list_contain_id(extract_ats_from_message_content(message_content), target_user_id)

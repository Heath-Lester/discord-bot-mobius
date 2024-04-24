"""File containing bot statuses to loop through while active"""

from discord import ActivityType
"""_summary_
    Status for the bot to display in the status column
    NOTE: Bots cannot use custom statuses or unknown statuses
"""
STATUSES_WITH_TYPES: dict[str, ActivityType] = {
    "with explosives 🧶": ActivityType.playing,
    "with dolphins 🐬": ActivityType.playing,
    "by himself 🌒": ActivityType.playing,
    "with fish 🐠": ActivityType.playing,
    "with your mom 🙇‍♀️": ActivityType.playing,
    "to your mom bitch 🤷‍♂️": ActivityType.listening,
    "Fight Club 🥊": ActivityType.watching,
    "Pulp Fiction 💉": ActivityType.watching,
    "the world burn 🔥": ActivityType.watching,
    "fish 🐟": ActivityType.watching,
    "for food 🦈": ActivityType.competing,
    "conspiracy documentaries 🤔": ActivityType.watching,
    "to bullshit 💩": ActivityType.listening,
    "to System of a Down 🤘": ActivityType.listening,
}

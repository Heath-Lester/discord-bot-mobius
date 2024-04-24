"""File containing bot statuses to loop through while active"""

from discord import ActivityType

STATUSES_WITH_TYPES: dict[str, ActivityType] = {
    "with explosives 🧶": ActivityType.playing,
    "with dolphins 🐬": ActivityType.playing,
    "by himself 🌒": ActivityType.playing,
    "with fish 🐠": ActivityType.playing,
    "your mom 🙇‍♀️": ActivityType.playing,
    "to your mom bitch 🤷‍♂️": ActivityType.listening,
    "Fight Club 🥊": ActivityType.watching,
    "the world burn 🔥": ActivityType.watching,
    "Is hungry 🎣": ActivityType.custom,
    "Plotting his next move 💭": ActivityType.custom,
    "Hates you 😠": ActivityType.custom,
    "Needs to shit 💩": ActivityType.custom,
}

"""File containing bot statuses to loop through while active"""

from discord import ActivityType

STATUSES_WITH_TYPES: dict[str, ActivityType] = {
    "with explosives 🧶": ActivityType.playing,
    "with dolphins 🐬": ActivityType.playing,
    "by himself 🌒": ActivityType.playing,
    "with fish 🐠": ActivityType.playing,
    "your mom 🙇‍♀️": ActivityType.playing,
    "to your mom bitch 🤷‍♂️": ActivityType.listening,
    "Fight club 🥊": ActivityType.watching,
    "the world burn 🔥": ActivityType.watching,
    "is hungry 🎣": ActivityType.custom,
    "plotting his next move 💭": ActivityType.custom,
    "hates you 😠": ActivityType.custom,
    "needs to shit 💩": ActivityType.custom,
}

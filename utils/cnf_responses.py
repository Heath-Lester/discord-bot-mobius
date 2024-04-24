def generate_command_not_found_responses(message_content: str) -> list[str]:
    bad_command: str = message_content
    if bad_command.startswith("!"):
        bad_command = bad_command[1:]

    return list(
        [
            "We don't take those here",
            f"'{bad_command}' is probably what I would have said if my sister was my mom too",
            "You misspelled 'I can't read'",
            "You misspelled 'I'm an idiot'",
            "Oh, try again sweetheart. Just try using your eyes this time.",
            "It's your world, we're just living in it",
            "Fat fingering is supposed to be an exception, not a condition",
            "Wha?",
            "Who?",
            "Please... don't try again",
            "Try looking at the keyboard this time...",
            "Helen Keller is better than you",
            "It's almost like you can't succeed",
            "Just give up",
            "You know there's a menu right?",
            "Why read the manual when you can fuck with it... ",
            "I don't get paid enough for this",
            "Did anyone else hear that?",
            "If you can't, you probably shouldn't",
            "When you fail, try, try again... because my time is yours to waste",
            "Maybe you need so see a neurologist?",
            "Well, I certainly can't help you",
            "Maybe one day you'll learn to read",
            "If you're our last hope then I'm just gonna quit now",
            "Ah, another one with delusions of adequacy",
            "Just. Try. Harder.",
            "Another one for the list",
            "Nope",
            "No",
            "If I could, I wouldn't",
            f"Hmmmm... {bad_command}, sounds like good idea if I were a moron",
            "It's really considerate of you to let me know you're going to waste my time",
            "It's okay, I make mistakes too. But this... this is a catastrophe",
            "Have you tried glasses?",
            "Try that again.. slower",
            "I bet if I was as dumb as you that would make sense",
            "Straight to jail",
            "I will ban you",
            "I swear to God...",
            "Have you tried turning it off and leaving it off?",
        ]
    )

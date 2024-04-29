def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(
        int(hours), int(minutes), int(seconds)
    )

activity_types = [
    {"id": 0, "name": "All", "icon_name": ""},
    {"id": 1, "name": "Sport", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Sport.jpg"},
    {"id": 2, "name": "Health", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Health.jpg"},
    {"id": 3, "name": "Sleep", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Sleep.jpg"},
    {"id": 4, "name": "Study", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Study.jpg"},
    {"id": 5, "name": "Rest", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Rest.jpg"},
    {"id": 6, "name": "Eat", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Eat.jpg"},
    {"id": 7, "name": "Coding", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Coding.jpg"},
    {"id": 8, "name": "Other", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Other.jpg"},
]
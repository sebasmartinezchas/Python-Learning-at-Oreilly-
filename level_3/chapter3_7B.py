from enum import Enum,auto
# Implement an enum for Color Theme
# That has the values LIGHT,DARK, DRACULA, and HIGH_CONTRAST
# Loop through four values
# Then set a color theme variable to Dracula
class ColorTheme(Enum):
    LIGHT = 1
    DARK = 2
    DRACULA = 3
    HIGH_CONTRAST = 4

# for theme in ColorTheme:
#     print(theme)

color_theme = ColorTheme.DRACULA
# print(f"Color theme 1: {color_theme}")
# color_theme = ColorTheme.HIGH_CONTRAST
# print(f"Color theme 2: {color_theme}")

# print(f"Color theme type: {type(color_theme)}")


class DayOfWeek(Enum):
    dow_index: int
    abbreviation: str
    is_weekend: bool

    SUNDAY = 1
    MONDAY = auto()
    TUESDAY = auto()


print(len(DayOfWeek))
print(f"Name: {DayOfWeek.SUNDAY.value}")
print(f"Name: {DayOfWeek.MONDAY.value}")
print(int(DayOfWeek.MONDAY==DayOfWeek.TUESDAY))

from enum import Enum

# Why use Enumerables?
"""
- Enumerables are objects but with a fixed set of values / instances.
- Useful examples:
    - Months of the year
    - Days of the week
    - Cards in a deck
    - States in the USA
    - Task results: success, failure, pending, etc.
    
"""

class DayOfWeek(Enum):
    dow_index: int
    abbreviation: str
    is_weekend: bool

    MONDAY = (0,'SUN',False)
    TUESDAY = (1,'MON',False)
    WEDNESDAY = (2,'TUE',False)
    THURSDAY = (3,'WED',False)
    FRIDAY = (4,'THU',False)
    SATURDAY = (5,'FRI',True)
    SUNDAY = (6,'SAT',False)


    def __new__(cls,dow_index,abbreviation,is_weekend):
        obj=object.__new__(cls)
        obj.dow_index=dow_index
        obj.abbreviation=abbreviation
        obj.is_weekend=is_weekend
        return obj


    @property
    def monday_first_dow_index(self):
        return (self.dow_index-1)%7


my_dow=DayOfWeek.SUNDAY
print(f"Name: {my_dow.name}")
print(f"Value: {my_dow.value}")
print(f"Abbreviation: {my_dow.abbreviation}")
print(f"Is weekend: {my_dow.is_weekend}")
print(f"Monday first DOW index: {my_dow.monday_first_dow_index}")
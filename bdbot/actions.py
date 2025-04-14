import enum


class Action(enum.Enum):
    Today = "Today"
    Random = "Random"
    Specific_date = "Specific date"
    Info = "Info"
    Add = "Add"
    Remove = "Remove"


class ExtendedAction(enum.Enum):
    Specific_date = "Specific_date"
    Remove_channel = "Remove_channel"
    Remove_guild = "Remove_guild"
    Remove_random = "Remove_random"
    Add_random = "Add_random"
    Add_all = "Add_all"
    Auto_remove_guild = "auto_remove_guild"
    Auto_remove_channel = "auto_remove_channel"

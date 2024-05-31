from enum import Enum


class MentionChoice(Enum):
    Enable = "Enable"
    Disable = "Disable"


class MentionPolicy(Enum):
    Daily = "Daily"
    All = "All"

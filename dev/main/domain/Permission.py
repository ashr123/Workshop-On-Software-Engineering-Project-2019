from enum import Enum, auto


class Permissions(Enum):
	REMOVE_ITEM = auto()
	ADD_ITEM = auto()
	EDIT_ITEM = auto()
	REMOVE_OWNER = auto()


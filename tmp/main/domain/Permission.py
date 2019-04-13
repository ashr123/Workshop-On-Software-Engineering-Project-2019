from enum import Enum, auto


class Permissions(Enum):
	ADD_ITEM = auto()
	REMOVE_ITEM = auto()
	EDIT_ITEM = auto()
	REMOVE_MANAGER = auto()
	ADD_MANAGER = auto()


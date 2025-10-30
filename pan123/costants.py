from enum import Enum


class SearchMode(Enum):
    NORMAL = 0
    EXACT = 1


class DuplicateMode(Enum):
    OVERWRITE = 2
    RENAME = 1


class VideoFileType(Enum):
    M3U8 = 1
    TS = 2

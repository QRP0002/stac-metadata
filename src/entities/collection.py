from datetime import datetime
from entities.bbox import BBox

class Collection:
    id = ''
    description = ''
    title = ''
    start_datetime = None
    end_datetime = None
    keys = None
    bbox = None

    def __init__(self, id, description, title):
        self.id = id
        self.description = description
        self.title = title
        self.start_datetime = datetime.now()
        self.end_datetime = datetime(1700, 5, 17)
        self.keys = set([])
        self.bbox = BBox(180, -180, 90, -90)
from datetime import datetime, timezone
from entities.bbox import BBox

class SBItem:
    image_uri = ''
    publication = ''
    start = ''
    end = ''
    bbox = None

    def __init__(self, image_uri, publication, start, end, bbox):
        self.image_uri = image_uri
        self.publication = self.date_to_iso(publication)
        self.start = self.date_to_iso(start)
        self.end = self.date_to_iso(end)
        self.bbox = BBox(bbox['minX'], bbox['maxX'],
                bbox['minY'], bbox['maxY'])

        
        
    def date_to_iso(self, date_str):
        dt = datetime.strptime(date_str['dateString'], '%Y-%m-%d')
        dt_utc = dt.replace(tzinfo=timezone.utc)
        iso_utc = dt_utc.isoformat()

        return iso_utc
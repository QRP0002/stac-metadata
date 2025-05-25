import pystac
from datetime import datetime
from shapely.geometry import box

class Collection:
    id = ''
    description = ''
    title = ''
    keywords = []
    extent = None

    def __init__(self, id, description, title, keywords, 
            bbox, start_time, end_time):
        
        self.id = id
        self.description = description 
        self.title = title
        self.keywords = keywords        
        self.extent = self.create_extent(bbox, start_time, end_time)

    def create_extent(self, bbox, start_time, end_time):
        new_extent = pystac.Extent(
            spatial=pystac.SpatialExtent([bbox]),
            temporal=pystac.TemporalExtent([[start_time, end_time]])
        )

        return new_extent
        

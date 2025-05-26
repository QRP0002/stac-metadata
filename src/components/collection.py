import json
import pystac

from datetime import datetime, timezone

class StacCollection:
    collection = None

    def create_stac_collection(self, collection):
        self.collection = pystac.Collection(
            id=collection.id,
            description=collection.description,
            title=collection.title,
            keywords=list(collection.keys),
            extent=pystac.Extent(
                spatial=pystac.SpatialExtent([[
                    collection.bbox.min_x,
                    collection.bbox.min_y,
                    collection.bbox.max_x,
                    collection.bbox.max_y
                ]]),
                temporal=pystac.TemporalExtent([[
                    collection.start_datetime,
                    collection.end_datetime
                ]])
            )
        )

        return self.collection

    def compare_start_date(self, current, compare):
        if isinstance(current, str):
            current = datetime.fromisoformat(current)
        if isinstance(compare, str):
            compare = datetime.fromisoformat(compare)
            
        # Make both aware in UTC if they're naive
        if current.tzinfo is None:
            current = current.replace(tzinfo=timezone.utc)
        if compare.tzinfo is None:
            compare = compare.replace(tzinfo=timezone.utc)
        
        return min(current, compare)

    def compare_end_date(self, current, compare):
        if isinstance(current, str):
            current = datetime.fromisoformat(current)
        if isinstance(compare, str):
            compare = datetime.fromisoformat(compare)
        
        # Make both aware in UTC if they're naive
        if current.tzinfo is None:
            current = current.replace(tzinfo=timezone.utc)
        if compare.tzinfo is None:
            compare = compare.replace(tzinfo=timezone.utc)

        return max(current, compare)

    def find_min(self, current, compare):
        return min(current, compare)

    def find_max(self, current, compare):
        return max(current, compare)

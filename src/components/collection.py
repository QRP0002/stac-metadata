import json
import pystac

from datetime import datetime, timezone

class StacCollection:
    collection = None

    def __init__(self, collection):
        self.collection = pystac.Collection(
            id=collection.id,
            description=collection.description,
            title=collection.title,
            keywords=collection.keywords,
            extent=collection.extent
        )
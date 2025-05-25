import json
import pystac

from datetime import datetime, timezone

class StacCatalog:
    catalog = None
    # Pass in a Catlog entity
    def __init__(self, catalog):
        self.catalog = pystac.Catalog(
            id=catalog.id,
            description=catalog.description,
            title=catalog.title,
        )
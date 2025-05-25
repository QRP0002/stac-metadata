import json
import os
import pystac
import rasterio

from dotenv import load_dotenv
from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping

class StacItem:
    item = None

    def __init__(self, image_path):
        load_dotenv()
        self.item = self.build_item(image_path)

    def build_item(self, image_path):
        bbox, footprint = self.get_bbox_and_footprint(image_path)
        datetime_utc = datetime.now(tz=timezone.utc)
        id = os.path.basename(image_path)
        
        new_item = pystac.Item(id=id,
            geometry=footprint,
            bbox=bbox,
            datetime=datetime_utc,
            properties={}
        )

        item_image_path = os.path.join(os.environ['IMAGE_BUCKET_BASE_URL'], id)
        new_item.add_asset(
            key='geotiff',
            asset=pystac.Asset(
                href=item_image_path,
                media_type=pystac.MediaType.GEOTIFF
            )
        )

        return new_item

    def get_bbox_and_footprint(self, image_path):
        with rasterio.open(image_path) as r:
            bounds = r.bounds
            bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
            footprint = Polygon([
                [bounds.left, bounds.bottom],
                [bounds.left, bounds.top],
                [bounds.right, bounds.bottom],
                [bounds.right, bounds.top],         
            ])

            return (bbox, mapping(footprint))
       
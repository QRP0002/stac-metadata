import json
import os
import pystac
import re

from dotenv import load_dotenv
from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from entities.bbox import BBox
from entities.sb_item import SBItem
from http_requests.http_requests import HttpRequests

class StacItem:
    item = None
    sb_id = ''
    title = ''
    summary = ''
    sb_item = None

    def __init__(self, id, title, summary):
        load_dotenv()
        self.sb_id = id
        self.title = title
        self.summary = summary

        self.fetch_sb_metadata()

        self.item = self.build_item()

    def fetch_sb_metadata(self):
        url = f'{os.environ['SB_JSON_URL']}/{self.sb_id}?format=json'
        response = HttpRequests.get_request(url)
        
        webLinksLen = len(response['webLinks'])
        image_uri = response['webLinks'][webLinksLen - 1]['uri']

        publication_date = response['dates'][0]
        start_date = response['dates'][1]
        end_date = response['dates'][2]

        tags = response['tags']

        _bbox= response['spatial']['boundingBox']        

        self.sb_item = SBItem(
            image_uri,
            publication_date,
            start_date,
            end_date,
            _bbox,
            tags
        )

    def build_item(self):
        bbox, footprint = self.get_bbox_and_footprint(self.sb_item.bbox)
        datetime_utc = datetime.now(tz=timezone.utc)
        id = self.scrub_item_id(self.title)
        
        new_item = pystac.Item(
            id=id,
            geometry=footprint,
            bbox=bbox,
            datetime=datetime_utc,
            properties={
                'title': self.title,
                'summary': self.summary,
                'publication_datetime': self.sb_item.publication,
                'start_datetime': self.sb_item.start,
                'end_datetime': self.sb_item.end,
                'tags': list(self.sb_item.tags)
            }
        )

        new_item.add_asset(
            key='geotiff',
            asset=pystac.Asset(
                href=self.sb_item.image_uri,
                media_type=pystac.MediaType.GEOTIFF
            )
        )

        return new_item

    def get_bbox_and_footprint(self, bbox):
        _bbox = (bbox.min_x, bbox.min_y, bbox.max_x, bbox.max_y)
        footprint = Polygon([
            [bbox.min_x, bbox.min_y],
            [bbox.min_x, bbox.max_y],
            [bbox.max_x, bbox.max_y],
            [bbox.max_x, bbox.min_y],         
            [bbox.min_x, bbox.min_y]
        ])

        return (_bbox, mapping(footprint))

    def scrub_item_id(self, id):
        if "1/3" in id:
            return re.sub("1/3", "1-3", id)
        if "1/9" in id: 
            return re.sub("1/9", "1-9", id)

        return id
       
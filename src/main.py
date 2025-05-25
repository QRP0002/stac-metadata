import json
import os
import pystac

from datetime import datetime

from entities.catalog import Catalog
from entities.collection import Collection
from components.catalog import StacCatalog
from components.collection import StacCollection
from components.item import StacItem
from cloud.upload_stac import UploadStac

catalogData = Catalog('usgs-dem', 'USGS DEM STAC', 
    'STAC for all types various types of DEM data.')
catalog = StacCatalog(catalogData).catalog

collectionData = Collection('1m-dem', 'Collection of the USGS 1m DEM COGs',
    'USGS 1m DEM', ['1m', 'dem', 'usgs'],
    [-180.0, -90.0, 180.0, 90.0], datetime(2020, 1, 1), datetime(2025, 1, 1))
collection = StacCollection(collectionData).collection

with open('../data/sb_1_meter_dem.json') as f:
    d = json.load(f)
    for sb_item in d['items']:
        item = StacItem(sb_item['id'], sb_item['title'], sb_item['summary']).item
        collection.add_item(item)
    f.close()

catalog.add_child(collection)
catalog.normalize_hrefs(f'../output/{catalog.id}')
catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

UploadStac().upload_catalog(catalog.id, f'../output/{catalog.id}/catalog.json')

collection_path = f'../output/{catalog.id}'
collection_dir_path =f'{catalog.id}'
for coll in catalog.get_collections():
    # Add collection meta data
    coll_path = f'{collection_dir_path}/{coll.id}'
    local_coll_path = f'{collection_path}/{coll.id}'

    UploadStac().upload_collection(coll_path, f'{local_coll_path}/collection.json')

    # Add collection item meta data
    for item in coll.get_items():
        item_bucket = f'{coll_path}/{item.id}'
        local_item_path = f'{local_coll_path}/{item.id}/{item.id}.json'
        
        UploadStac().upload_item(item_bucket, local_item_path)        

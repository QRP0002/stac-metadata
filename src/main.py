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

with open('../data/config.json') as config:
    _config = json.load(config)

    _catalog = _config['catalog']
    catalogData = Catalog(_catalog['id'], _catalog['title'], 
        _catalog['description'])
    catalog = StacCatalog(catalogData).catalog

    for _coll in _config['collections']:
        _collection = _coll['collection']
        print('COLLECTION: ', _collection)
        sc = StacCollection()
        tc = Collection(_collection['id'], _collection['description'],
            _collection['title'])

        items_cache = []
        _items = _coll['items']
        with open(_items['data']) as f:
            d = json.load(f)
            for sb_item in d['items']:
                item = StacItem(sb_item['id'], sb_item['title'], sb_item['summary']).item
                items_cache.append(item)

                # Compare item data to collection data to get the most accurate information
                _start = sc.compare_start_date(tc.start_datetime, 
                    item.properties['start_datetime'])
                tc.start_datetime = _start

                _end = sc.compare_end_date(tc.end_datetime, 
                    item.properties['end_datetime'])
                tc.end_datetime = _end

                for tag in item.properties['tags']:
                    tc.keys.add(tag)

                tc.bbox.min_x = sc.find_min(tc.bbox.min_x, item.bbox[0])
                tc.bbox.min_y = sc.find_min(tc.bbox.min_y, item.bbox[1])
                tc.bbox.max_x = sc.find_max(tc.bbox.max_x, item.bbox[2])
                tc.bbox.max_y = sc.find_max(tc.bbox.max_y, item.bbox[3])
        
            f.close()

        collection = sc.create_stac_collection(tc)
        collection = sc.add_items(items_cache, collection)

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
    config.close()
import json
from stac_validator import stac_validator
from pystac import Catalog, get_stac_version
from pystac.extensions.eo import EOExtension
from pystac.extensions.label import LabelExtension

root_catalog = Catalog.from_file('https://quinn-stac-catalog.nyc3.digitaloceanspaces.com/stac-catalogs/usgs-dem/catalog.json')
root_catalog.describe()

print('------------- Catalog -------------')
stac = stac_validator.StacValidate('https://quinn-stac-catalog.nyc3.digitaloceanspaces.com/stac-catalogs/usgs-dem/catalog.json')
stac.run()

json_str = json.dumps(stac.message, indent=4)
print(json_str)
print('------------- Catalog -------------')

print('------------- Collection -------------')
stac = stac_validator.StacValidate('https://quinn-stac-catalog.nyc3.digitaloceanspaces.com/stac-catalogs/usgs-dem/1m-dem/collection.json')
stac.run()
json_str = json.dumps(stac.message, indent=4)
print(json_str)
print('------------- Collection -------------')

print('------------- ITEM  -------------')
stac = stac_validator.StacValidate('https://quinn-stac-catalog.nyc3.digitaloceanspaces.com/stac-catalogs/usgs-dem/1m-dem/USGS_1M_13_x51y441_CO_EasternColorado_2018_A18.tif/USGS_1M_13_x51y441_CO_EasternColorado_2018_A18.tif.json')
stac.run()
json_str = json.dumps(stac.message, indent=4)
print(json_str)
print('------------- ITEM -------------')

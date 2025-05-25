## STAC Workflow
### Item
Needs:
- id
- type
- geometry
- bbox
- properties
Others:
- stac_version
- links
- assets
- instruments
- platform
- gsd
### Catalog
Needs:
- id
- type
- stac_version
- description
- links
Others:
- title

Catalog Example
```
{
    "stac_version": "1.0.0",
    "type": "Catalog",
    "id": "20201211_223832_CS2",
    "description": "A simple catalog example",
    "links": []
}
```

### Collections
Needs:
- id
- type
- stac_version
- description
- links
- summaries
Others:
- title 
- stac_extensions
- license
- extent
- providers
- keywords
- assets

Collections Example:
```
{
    "stac_version": "1.0.0",
    "type": "Collection",
    "license": "ISC",
    "id": "20201211_223832_CS2",
    "description": "A simple collection example",
    "links": [],
    "extent": {},
    "summaries": {}
}
```


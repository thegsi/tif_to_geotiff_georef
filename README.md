# tif_to_geotiff_georef


Georeferencer API
http://api.oldmapsonline.org/1.0/maps
https://app.swaggerhub.com/apis-docs/OldMapsOnline/OldMapsOnline/1.0#/Maps/get_maps__id__georeferences
​/maps​/{id}
/maps/external/{external_id}
​/maps​/{id}​/georeferences

gdal must match system gdal
`gdainfo --version`
`pip install gdal==2.4`

`pip install PIL` etc

Place files in `./osds_tiffs` folder.
`python3 georef_tif_to_geotiff.py'

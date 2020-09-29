import gdal
import osr
import pickle
import numpy
from PIL import Image
from PIL import ImageDraw
import csv
import shutil
import os

with open('OSDs_with_paths.csv', newline='') as f:
    reader = csv.reader(f)
    map_metadatas = list(reader)
with open(f'osd_georefs.pickle','rb') as in_pickle:
    georefs = pickle.load(in_pickle)
    georefsid = {}
    for georef in georefs:
        georefsid[georef['external_id']] = georef

os.mkdir('./osds_tiffs_cut/')
os.mkdir('./osds_gcps/')
os.mkdir('./osds_geotiffs/')

# Create cut tiffs
for map in map_metadatas:
    path = map[1].split('\\')[-1]
    print(path)
    img = Image.open('./osds_tiffs/' + path)
    mask=Image.new('L', img.size, color=0)
    draw=ImageDraw.Draw(mask)

    points = tuple(tuple(sub) for sub in georefsid[map[0]]['cutline'])
    draw.polygon((points), fill=255)
    img.putalpha(mask)

    rgb = Image.new('RGB', img.size, (255, 255, 255))
    rgb.paste(img, mask=img.split()[3])
    rgb.save('./osds_tiffs_cut/' + path, 'TIFF', resolution=100.0)

def createGcps(coords):
    gcps = []
    for coord in coords:
        # 'coord' = {'location': [-3.756732387660781, 50.57983418053561], 'pixel': [2164, 966]}
        col = coord['pixel'][0]
        row = coord['pixel'][1]
        x = coord['location'][0]
        y = coord['location'][1]
        z = 0
        gcp = gdal.GCP(x, y, z, col, row)
        gcps.append(gcp)
    return gcps

# https://stackoverflow.com/questions/55681995/how-to-georeference-an-unreferenced-aerial-imgage-using-ground-control-points-in

def addGcps(path, gcps):
  # os.mkdir('./osds_tiffs_cut/')
  src = './osds_tiffs_cut/' + path
  dst = './osds_gcps/' + path
  # Create a copy of the original file and save it as the output filename:
  shutil.copy(src, dst)
  # Open the output file for writing for writing:
  ds = gdal.Open(dst, gdal.GA_Update)
  # Set spatial reference:
  sr = osr.SpatialReference()
  sr.ImportFromEPSG(4326)

  # Apply the GCPs to the open output file:
  ds.SetGCPs(gcps, sr.ExportToWkt())

  # Close the output file in order to be able to work with it in other programs:
  ds = None

def createGeoTiff(path):
  src = './osds_gcps/' + path
  dst = './osds_geotiffs/' + path
  input_raster = gdal.Open(src)
  gdal.Warp(dst,input_raster,dstSRS='EPSG:4326',dstNodata=255)

cutpaths = os.listdir('./osds_tiffs_cut')
for path in cutpaths:
    for map in map_metadatas:
        if path == map[1].split('\\')[-1]:
            print(map)
            georef = georefsid[map[0]]
            coords = georef['gcps']
            gcps = createGcps(coords)
            addGcps(path, gcps)
            createGeoTiff(path)

shutil.rmtree('./osds_gcps/')
shutil.rmtree('./osds_tiffs_cut/')

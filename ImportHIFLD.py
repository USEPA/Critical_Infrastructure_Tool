import arcpy
from sys import argv
import os
import pandas
import json
import arcpy, sys, os, arcgis, requests 
import urllib
import urllib.request
import subprocess
from shutil import copyfile


def importDataset(Input_Path, Temporary_Output_Path):
    #download_url(r"https://landscape1.arcgis.com/arcgis/rest/services/USA_Roads/MapServer", "USA_Roads")
    createLayerFromShapefile(Input_Path, "USA_Roads", Temporary_Output_Path)
    download_url(r"https://landscape11.arcgis.com/arcgis/rest/services/USA_Soils_Farmland_Class/ImageServer", "USA_Soils_Farmland_Class")
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0.geojson", "Hospital_Locations_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/155761d340764921ab7fb2e88257bd97_0.geojson", "Landfills_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/4b9bac25263047c19e617d7bd7b30701_0.geojson", "Wastewater_Treatment_Plants_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/ee0263bd105d41599be22d46107341c3_0.geojson", "Power_Plants_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/1b6e231f88814aceb30fb6ad3ff86014_0.geojson", "Major_State_Government_Buildings_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/0835ba2ed38f494196c14af8407454fb_0.geojson", "Cellular_Towers_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/ec4d868ea1354fc9a85fe35e7db0cffd_0.geojson", "Land_Mobile_Broadcast_Tower_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/0ccaf0c53b794eb8ac3d3de6afdb3286_0.geojson", "Fire_Stations_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/335ccc7c0684453fad69d8a64bc89192_0.geojson", "Urgent_Care_Facilities_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/362c9480f12e4587b6a502f9ceedccde_0.geojson", "Emergency_Medical_Center_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/02013eaa0e1e4cc59658fe9e1c7ac703_0.geojson", "Ports_HIFLD", Temporary_Output_Path)
    #createLayerFromAPI(r"https://opendata.arcgis.com/datasets/e720d6671dc54e3084bd079b845e136f_0.geojson", "Primary_Roads_HIFLD", Temporary_Output_Path)

def createLayerFromShapefile(Input_Path, name, Temporary_Output_Path):
    path_to_layer= Temporary_Output_Path + "\\"+name + "_layer.lyr"
    arcpy.MakeFeatureLayer_management(Input_Path + "\\tl_2016_us_primaryroads.shp",name)
    newlayer = arcpy.SaveToLayerFile_management(name, Input_Path + "\\tl_2016_us_primaryroads.shp", "ABSOLUTE")
    p = arcpy.mp.ArcGISProject("CURRENT")
    m = p.activeMap
    lyr = m.addDataFromPath(newlayer)
    getLayerStyle(name, lyr)
    lyr.visible = True

    # Refresh things

def download_url(url, layer_name):
    arcpy.env.overwriteOutput = True
##    with urllib.request.urlopen(url) as dl_file:
##        with open(save_path+"\\Primary Roads", 'wb') as out_file:
##            out_file.write(dl_file.read())
    
    p = arcpy.mp.ArcGISProject("CURRENT")
    m = p.activeMap
    if arcpy.Exists(layer_name):
        arcpy.Delete_management(layer_name)
    lyr = m.addDataFromPath(url)

def createLayerFromAPI(url, name, OutputPath):
    outputLocation= OutputPath + "\\"+name
    response = urllib.request.urlopen(url)
    path_parent = os.path.dirname(arcpy.env.workspace)
    data = json.loads(response.read())
    path = outputLocation + ".json"
    with open(path, 'w+') as f:
        json.dump(data, f, indent=2)
    outputLayer = outputLocation + ".shp"
    arcpy.JSONToFeatures_conversion(path, outputLayer, "POINT")
    path_to_layer= OutputPath + "\\"+name + "_layer.lyr"
    arcpy.MakeFeatureLayer_management(outputLayer,name)
    newlayer = arcpy.SaveToLayerFile_management(name, path_to_layer, "ABSOLUTE")
    p = arcpy.mp.ArcGISProject("CURRENT")
    m = p.activeMap
    lyr = m.addDataFromPath(newlayer)
    getLayerStyle(name, lyr)
    lyr.visible = True

def getLayerStyle(name, lyr):
    sym = lyr.symbology
    communication = sym.renderer.symbol.listSymbolsFromGallery("Radio Tower")
    hospital = sym.renderer.symbol.listSymbolsFromGallery("Hospital")
    energy = sym.renderer.symbol.listSymbolsFromGallery("Industrial Complex")
    gov = sym.renderer.symbol.listSymbolsFromGallery("City Hall")
    if "Hospital" in name or "Urgent" in name:
        for symbol in hospital:
            if symbol.size == 14.0:
                sym.renderer.symbol = symbol
                lyr.symbology = sym
    if "Tower" in name:
        for symbol in communication:
            if symbol.size == 14.0:
                sym.renderer.symbol = symbol
                lyr.symbology = sym
    if "Government" in name:
        for symbol in gov:
            if symbol.size == 14.0:
                sym.renderer.symbol = symbol
                lyr.symbology = sym
    if "Power" in name:
        for symbol in energy:
            if symbol.size == 14.0:
                sym.renderer.symbol = symbol
                lyr.symbology = sym
    if "water" in name:
        sym.renderer.symbol.applySymbolFromGallery("Circle 1")
        sym.renderer.symbol.color = {'RGB' : [0,0,139, 100]}
        sym.renderer.symbol.size = 4

        lyr.symbology = sym
    if "Fire" in name or "Emergency" in name:
        
        sym.renderer.symbol.applySymbolFromGallery("Circle 1")
        sym.renderer.symbol.color = {'RGB' : [255,0,0, 100]}
        sym.renderer.symbol.size = 4

        lyr.symbology = sym
    if "Landfill" in name:
        sym.renderer.symbol.applySymbolFromGallery("Circle 1")
        sym.renderer.symbol.color = {'RGB' : [139,69,19, 100]}
        sym.renderer.symbol.size = 4

        lyr.symbology = sym

    if "Ports" in name:
        sym.renderer.symbol.applySymbolFromGallery("Circle 1")
        sym.renderer.symbol.color = {'RGB' : [0,255,255, 100]}
        sym.renderer.symbol.size = 4

        lyr.symbology = sym
                

if __name__ == '__main__':
    with arcpy.EnvManager(scratchWorkspace=arcpy.env.workspace, workspace=arcpy.env.workspace):
        importDataset(*argv[1:])

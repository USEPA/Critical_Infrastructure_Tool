import arcpy
from sys import argv
import os
import pandas
import json
#import arcpy, sys, os, arcgis, requests 
import urllib
import urllib.request
import subprocess
from shutil import copyfile


def importDataset(Temporary_Output_Path):
    desc = arcpy.Describe("SIRM Tool.tbx")
    Input_Path = desc.path + "\\Input Shapefiles"
    #download_url(r"https://landscape1.arcgis.com/arcgis/rest/services/USA_Roads/MapServer", "USA_Roads")
    createLayerFromShapefile(Input_Path+ "\\tl_2016_us_primaryroads.shp", "USA_Roads", Temporary_Output_Path)
    createLayerFromShapefile(Input_Path+ "\\farms.shp", "USA_Farms", Temporary_Output_Path)
    createLayerFromShapefile(Input_Path+ "\\agriculture_buildings.shp", "Agriculture_Buildings_FRS", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/636e283fc23645dfaeebdac5d9254776_0.geojson","Industrial_HIFLD", Temporary_Output_Path)
    #download_url(r"https://landscape11.arcgis.com/arcgis/rest/services/USA_Soils_Farmland_Class/ImageServer", "USA_Soils_Farmland_Class")
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0.geojson", "Hospital_Locations_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/155761d340764921ab7fb2e88257bd97_0.geojson", "Landfills_HIFLD", Temporary_Output_Path)
    #createLayerFromAPI(r"https://opendata.arcgis.com/datasets/dfedf186401240bc8d382e80188ac512_1.geojson", "Wastewater_Treatment_Plants_HIFLD", Temporary_Output_Path)
    createLayerFromShapefile(Input_Path+"//water_treatment_plants.shp","Water_Treatment_Plants_FRS", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/ee0263bd105d41599be22d46107341c3_0.geojson", "Power_Plants_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/1b6e231f88814aceb30fb6ad3ff86014_0.geojson", "Major_State_Government_Buildings_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/0835ba2ed38f494196c14af8407454fb_0.geojson", "Cellular_Towers_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/ec4d868ea1354fc9a85fe35e7db0cffd_0.geojson", "Land_Mobile_Broadcast_Tower_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/0ccaf0c53b794eb8ac3d3de6afdb3286_0.geojson", "Fire_Stations_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/335ccc7c0684453fad69d8a64bc89192_0.geojson", "Urgent_Care_Facilities_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/3afdb0478d6940e7ace338976833925d_0.geojson", "Emergency_Medical_Center_HIFLD", Temporary_Output_Path)
    #createLayerFromAPI(r"https://opendata.arcgis.com/datasets/b2de4fc3bdf34c6590ce6e26b4e6e484_0.geojson", "Ports_HIFLD", Temporary_Output_Path)
    #createLayerFromAPI(r"https://opendata.arcgis.com/datasets/e720d6671dc54e3084bd079b845e136f_0.geojson", "Primary_Roads_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/87376bdb0cb3490cbda39935626f6604_0.geojson", "Public_Schools_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/0dfe37d2a68545a699b999804354dacf_0.geojson", "Private_Schools_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/bc7ef39f9d2a4605b9d5aad0e050af11_0.geojson",
                       "Colleges_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/a4d813c396934fc09d0b801a0c491852_0.geojson",
                       "Corporate_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/97603afcff00443f874acbe03c9e794a_0.geojson",
                       "Worship_HIFLD", Temporary_Output_Path)
    createLayerFromAPI(r"https://opendata.arcgis.com/datasets/468e9601b9b7407396e5c4f59772f1ff_0.geojson","Transmission_HIFLD", Temporary_Output_Path)
    createLayerFromAPI("https://opendata.arcgis.com/datasets/39567c09b9d1491b892b3bbb065e77ef_0.geojson", "Electric_Substation_HIFLD", Temporary_Output_Path)
    #download_url(r"https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/MSBFP2/FeatureServer/0/query?outFields=*&where=1%3D1", "Building_Footprints")

        
def createLayerFromShapefile(Input_Path, name, Temporary_Output_Path):
    path_to_layer= Temporary_Output_Path + "\\"+name + "_layer.lyr"
    arcpy.MakeFeatureLayer_management(Input_Path,name)
    newlayer = arcpy.SaveToLayerFile_management(name, Input_Path, "ABSOLUTE")
    p = arcpy.mp.ArcGISProject("CURRENT")
    m = p.activeMap
    lyr = m.addDataFromPath(newlayer)
    getLayerStyle(name, lyr)
    lyr.visible = True

    # Refresh things

def createLayerFromLayerFile(Input_Path, name, Temporary_Output_Path):
    p = arcpy.mp.ArcGISProject("CURRENT")
    m = p.activeMap
    if arcpy.Exists(name):
        return
    lyr = m.addDataFromPath(Input_Path)
    #getLayerStyle(name, lyr)
    lyr.visible = True

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




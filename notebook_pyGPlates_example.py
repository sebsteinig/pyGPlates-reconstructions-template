# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [markdown] colab_type="text" id="view-in-github" tags=[]
# <a href="https://colab.research.google.com/github/sebsteinig/pyGPlates-reconstructions-template/blob/main/notebook_pyGPlates_example.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
# -

# # pyGPlates site reconstructions
# Reconstruct paleolocations of present-day locations across the Phanerozoic. PyGplates allows to use some of the functionality of the GUI GPlates software within python scripts. This allows scripting to automatically process many different locations and/or time periods. Different rotation models can be used and are easily exchangeable. I currently use the PALEOMAP rotation model that is consistent to the Bristol Scotese simulations by Paul Valdes.

# ## Prelude (only necesseary when running on Google Colab)
# If running on Google Colab, execute the following cell to download the repo and install pyGPlates on the virtual machine. 
#
# If running somewhere else, you can execute the whole notebooks and this part will be skipped automatically.

# +
# detect if we are running on colab
try:
    import google.colab
    IN_COLAB = True
except:
    IN_COLAB = False
    print('not running on Google Colab')

if IN_COLAB:
# configure environment on Colab
    import google.colab

    # if on Colab, clone the repository to access the data locally
    import os
    repo = "pyGPlates-reconstructions-template"

    # clone repo if it does not already exist
    if not os.path.exists(repo):
        print('cloning GitHub repository '+repo)
        # !git clone https://github.com/sebsteinig/{repo}.git
  
    # %cd {repo}
    
    # install pygplates
    # !sudo apt install bin/pygplates_0.36.0_py36_ubuntu-18.04-amd64.deb
    
# -

# ## User input
# define variables/lists to quickly change inputs to the notebook

# +
# input csv file with label, modern latitude, modern longitude
file_input_sites = 'input_sites_example.csv'

# list of ages (in Ma) for which we want to reconstruct paleolocations for the input sites
ages           = ['0', '100', '200', '300']


# -

# ## import pygplates and other packages

# +
import os
import sys
import pandas as pd

# add pygplates to python path
if IN_COLAB:
  sys.path.insert(0, os.path.abspath('/usr/lib')) # ubuntu VM on colab
else:
  sys.path.insert(0, os.path.abspath('./bin/pygplates_0.36.0_py37_Darwin-x86_64')) # macOS Intel 
import pygplates


# -

# ## load plate model
# List of available models at http://portal.gplates.org/portal/rotation_models/.
# Here we are using the 'PALEOMAP PaleoAtlas for GPlates'by Scotese et al. (https://www.earthbyte.org/paleomap-paleoatlas-for-gplates/)

# + colab={"base_uri": "https://localhost:8080/"} id="WcMt0hmK_38Q" outputId="1ca62e3a-a818-48f8-aea4-d2827f558cdb"
# static polygons are the 'partitioning features'
static_polygons = pygplates.FeatureCollection('PALEOMAP_Global_Plate_Model/PALEOMAP_PlatePolygons.gpml')
# actual rotation model
rotation_model=pygplates.RotationModel('PALEOMAP_Global_Plate_Model/PALEOMAP_PlateModel.rot')
# -

# ## Main code
# 3-step process to reconstruct paleolocations:
# 1. combine input points into feature collection
# 2. assign plate ids to features
# 3. reconstruct paleolocations for features

# +
# load point coordinates
df_sites = pd.read_csv(file_input_sites,sep=',')

for ageCount, age in enumerate(ages):
    
    # Create target directory & all intermediate directories if don't exists
    dirName = './reconstructed-shapes/'+ ages[ageCount] + 'Ma'
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists") 
    
    #### step 1: put the points into a feature collection, using Lat,Lon coordinates from dataframe
    point_features = []
    for index,row in df_sites.iterrows():
        point = pygplates.PointOnSphere(float(row.LAT),float(row.LON))
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point)
        point_features.append(point_feature)

    ### step 2: assign plate ids to features
    # To reconstruct any feature geometries, each feature must have a plate id assigned. If they don't already, 
    # then the pygplates function 'PlatePartitioner' performs this function (analogous to the 'assign plate ids' 
    # menu option in GPlates GUI) 
    partitioned_point_features = pygplates.partition_into_plates(static_polygons, rotation_model, point_features) 

    ### step 3: reconstruct paleolocations for features
    # Two possible ways:
    
    # 1. save shape files to disk for later use (e.g. load sahpefiles into python script for direct plotting)
    pygplates.reconstruct(partitioned_point_features, rotation_model, dirName +'/NA-sites.shp', float(ages[ageCount]))
    
    # 2. output paleolocations directly
    reconstructed_feature_geometries = []
    pygplates.reconstruct(partitioned_point_features, rotation_model, reconstructed_feature_geometries, float(ages[ageCount]))    
    for siteCount, reconstructed_feature_geometry in enumerate(reconstructed_feature_geometries):
        paleoLocation = reconstructed_feature_geometry.get_reconstructed_geometry().to_lat_lon()
        print('Paleolocation for ' + df_sites.name[siteCount] + ' at ' + ages[ageCount] + 'Ma (LAT/LON): ' + str(round(paleoLocation[0],1)) + '/'+str(round(paleoLocation[1],1)) )

# -





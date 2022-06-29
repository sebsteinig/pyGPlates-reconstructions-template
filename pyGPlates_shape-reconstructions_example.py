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
# <a href="https://colab.research.google.com/github/sebsteinig/pyGPlates-reconstructions-template/blob/main/pyGPlates_shape-reconstructions_example" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
# -

# # pyGPlates shape reconstructions
# Reconstruct shapes (defined as list of individual points) of present-day locations across the Phanerozoic. PyGplates allows to use some of the functionality of the GUI GPlates software within python scripts. This allows scripting to automatically process many different locations and/or time periods. Different rotation models can be used and are easily exchangeable. I currently use the PALEOMAP rotation model that is consistent to the Bristol Scotese simulations by Paul Valdes.

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
files_input_shapes = ['example_shape1', 'example_shape2']

# list of ages (in Ma) for which we want to reconstruct paleolocations for the input sites
ages           = ['0', '100', '200', '300']



# -

# ## import pygplates and other packages

# +
import os
import sys
import pandas as pd
import csv

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
# 4-step process to reconstruct paleolocations:
# 1. combine input points into feature collection
# 2. create polygon from points
# 3. assign plate ids to features
# 4. reconstruct paleolocations for features

# loop over all input shapes
for shapeCount, shapeName in enumerate(files_input_shapes):
    
    # load shapes coordinates
    df_shape = pd.read_csv('./'+ shapeName +'.csv',sep=',')
    
    for ageCount, age in enumerate(ages):

        # Create output directories & all intermediate directories if don't exists
        output_dir = './reconstructions/'+ ages[ageCount] + 'Ma'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print("Directory " , output_dir ,  " Created ")
        else:    
            print("Directory " , output_dir ,  " already exists") 

        # put the points into a feature collection, using Lat,Lon coordinates from dataframe
        polygon_points = []
        polygon_feature = []
        for index,row in df_shape.iterrows():
            point = pygplates.PointOnSphere(float(row.LAT),float(row.LON))
            polygon_points.append(point)

        #add_polyline_feature_from_points(polyline_features, polyline_points, row)
        polygon = pygplates.PolygonOnSphere(polygon_points)
        polygon_feature = pygplates.Feature() # 'unclassified' feature
        polygon_feature.set_geometry(polygon)

        # The partition points function can then be used as before
        partitioned_polygon_feature = pygplates.partition_into_plates(static_polygons, rotation_model, polygon_feature) 

        # Reconstruct the shapes
        reconstructed_polyline_feature_geometries = []
        pygplates.reconstruct(partitioned_polygon_feature, rotation_model, output_dir +'/' + shapeName + '_' + ages[ageCount] +'Ma.shp', float(ages[ageCount]) ) 


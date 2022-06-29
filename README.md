# pyGPlates python notebooks 

## purpose
Reconstruct paleolocations of present-day locations and shapes across the Phanerozoic. [PyGplates](https://www.gplates.org/docs/pygplates/) allows to use some of the functionality of the GUI [GPlates](https://www.gplates.org/) software within python scripts. This allows scripting to automatically process many different locations and/or time periods. Different [rotation models](http://portal.gplates.org/portal/rotation_models/) can be used and are easily exchangeable. I currently use the [PALEOMAP](https://www.earthbyte.org/paleomap-paleoatlas-for-gplates/) rotation model that is consistent to the Bristol [Scotese simulations](https://cp.copernicus.org/articles/17/1483/2021/) by Paul Valdes. 

## input data
Present-day locations for `pygplates_paleolocations.ipynb` need to be defined in a CSV file (name, lat, lon) as shown in the example file `inpt_sites.csv`. When reconstructing shapes (e.g. a country outline) with `pygplates_paleoshapes.ipynb` each shape needs to be defined in a separate CSV file (name, lat, lon) with the points describing the modern outline of the shape. We also need to specify the location of the chosen plate model files, e.g. 'data/PALEOMAP_Global_Plate_Model' ([download link](https://www.earthbyte.org/paleomap-paleoatlas-for-gplates/)). The PyGPlates software itself is not yet availabe via packet managers like `conda`. Pre-compiled binaries are [available](https://www.gplates.org/docs/pygplates/pygplates_getting_started.html#installing-pygplates) for different operating systems and python versions. This repo was used on macOS and google colab using the `conda` environemt specified in `environemnt.yml` (see below) with the respective bianaries in the `bin` directory. These need to be [updated accordingly]([available](https://www.gplates.org/docs/pygplates/pygplates_getting_started.html#installing-pygplates)) when running in a different environemnt.

## running the notebooks
Notebooks can either be run on [Google Colab](https://colab.research.google.com/) (online, Google account required) or locally. Notebooks should include a button to open it in Colab, otherwise you can also directly load a GitHub repo within Colab. Easiest way to run locally is to first download the repo with

```
git clone https://github.com/USERNAME/REPOSITORY
``` 

and then install [conda](https://conda.io/projects/conda/en/latest/index.html) (if not installed already). Then create an environment `env_name` with 

```
conda env create --name env_name --file=environment.yml
``` 

using the `environment.yml` file from this repository to install all necessary python packages. The notebooks can then be run interactively by typing

```
jupyter lab
```

We further use the [jupytext](https://jupytext.readthedocs.io/en/latest/index.html) package to automatically save a pure python script (*.py) each time the notebook is saved. This is very helpful for clean diffs in the version control and allows you to run the analysis in your local terminal with:

```
python notebook_name.py
```
The python file can also be shared with others to work on the code together using all the version control benefits (branches, pull requests, ...). You can edit it with any tex editor/IDE and it can also be converted back to a jupyter notebook (with no output) via
```
jupytext --to notebook notebook_name.py
```


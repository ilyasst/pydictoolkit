# pydictoolkit

Toolkit to further analyze 2D and 3D Digital Image Correlation results. The current work focuses on strain evolution at the surface of growing biological materials.

# Main features

- [x] Compute the difference between consecutive images (the "delta") for the available fields (displacement and strain fields)
- [x] Ability to divide the AOI into equal rectangular areas of prescribed size and to plot heatmaps of the "delta" for any field
- [x] Compute the minimal and maximal values of a field for a set of CSV results (good values to know if we want to have a single scale for all the provided CSV files)
- [x] Contour plot for the displacement or strain fields with automatically scaled color bar
- [x] Streamline plots of the `U` and `V` displacement field
- [ ] Streamline plots of the first or second principal strain fields
- [ ] Allow the user to be able to change the name of the spatial variables (`x` instead of `X` in the case of VIC2D since there is no `X (mm)` by default)
- [ ] Increase the quality (dpi) of the plots, or even better turn it into a deck variable


# Quickstart

If you know what you're doing, then this section is for you. Otherwise, you should go to the `Getting Started` section.

#### Linux:

```
sudo apt install python3-pip python3-venv
git clone https://github.com/ilyasst/pydictoolkit.git
cd pydictoolkit
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python main.py -h
```

Basic usage:
```
python main.py -d "./deck.yaml"
```

# Getting started

## Installation

The following pieces of software are required to run pydictoolkit:

* Python 3.6 or higher
* python3-pip
* python3-venv

The list of necessary python packages is provided in the `requirements.txt` file and can be installed using pip:

```
pip install -r requirements.txt
```

We recommend that you create a virtual environment before installing these packages using the python3-venv software:

```
python3 -m venv .env
```

You can then load your virtual environment using:
```
source .env/bin/activate
```

In order to exit it, use the `deactivate` command.

## Usage

In order to use the code, you will need to provide:

* A valid `deck.yaml` file (the content of this file is further detailed in the `Input description` section)
* Your VIC3D CSV grid outputs (`.csv`) and stereo-images (`.tiff`) in the folder specified in the `deck.yaml` file

You can then run pydictoolkit using:
```
python main.py -d "PATH_TO_DECK"
```
where `PATH_TO_DECK` is the path to your deck.yaml file.

A short help/reminder can be accessed using:
```
python main.py -h
```

# Input description

## deck.yaml

Main structure of the `deck.yaml` file:

```yaml
Data:
  Folder: ./pydictoolkit/dummy_data/

Plots:
  Target Plot: e1
  Groups:
    Region:
      i: 200
      j: 200
  Target Column: e1_delta

```

The remainder of this section provides detailed explanations for each section.

#### Data

```yaml
Data:
  Folder: ./pydictoolkit/dummy_data/
```

The Data section contains a single value: the path of the folder that contains your VIC3D CSV grid data and stereo-images. It can be an absolute path, or a path relative to the main.py file.


## Your VIC3D grid data

Let's make add a few screenshots to show which CSV files we mean exactly.

## Examples

An example:

* Description of the example data and credit where it's due

## Contribute ?

Maybe you need something for your own project, maybe you found a mistake or something you could improve and feeling like helping, in any case, we'll be happy to get in touch. Please leave us an Issue, or a Pull Request (we welcome those!).


# Disclaimer

This software is for educational and research purposes only. Use it at your own risks.


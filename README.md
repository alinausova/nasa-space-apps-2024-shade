## Shade Gap Project
### Built in scope of the [2024 NASA Space Apps Challenge](https://www.spaceappschallenge.org/nasa-space-apps-2024/)

![screenshot1.png](src/assets/screenshot1.png)
[Shade Gap Prototype Demo](https://alinausova.github.io/nasa-space-apps-2024-shade/)

This project introduces an original **risk indexing tool** that leverages scientific literature and incorporates new parameters developed through competition research. The tool is designed to categorize areas based on potential risk factors, particularly during future heat stress crises, with a focus on health and energy risk prediction.

The platform utilizes **geoTIFF data** pulled from a selected area within the Delhi metropolitan region using [ShadeMap](https://shademap.app/). Snapshots were taken every hour from 9 AM to 5 PM, and the fraction of shaded area was averaged across all time samples for each area. The data was then spatially binned (clustered by 8 pixels) and encoded as **geoJSON** to be displayed on the map.

This processing provides a **shade index** (ranging from 0 to 1) that indicates the amount of shade an area receives throughout the day, which is a crucial factor in predicting higher-risk areas during heat stress conditions.


## Features
![screenshot2.png](src/assets/screenshot2.png)
- **Interactive Map**: Map integrated with Mapbox.
- **Data Visualisation**: Markers with different colors for visual distinction.

## Technologies

- **Frontend**: Svelte
- **Map Integration**: [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
- **Build Tool**: Vite for fast development and optimized production builds.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v20+)
- npm or yarn
- A [Mapbox account](https://account.mapbox.com/) to get your access token.

### Installation

Install the dependencies:

   ```bash
   npm install
   ```

Create a `.env` file in the root directory and add your Mapbox access token:

   ```env
    VITE_MAPBOX_ACCESS_TOKEN=your-access-token
   ```


Start the development server:
   ```bash
   npm run dev
   ```

To build the project:
   ```bash
   npm run build
   ```

### Python environment
## Shade Gap Project
### Built in scope of the [2024 NASA Space Apps Challenge](https://www.spaceappschallenge.org/nasa-space-apps-2024/)
![screenshot1.png](src/assets/screenshot1.png)
[Shade Gap Prototype Demo](https://alinausova.github.io/nasa-space-apps-2024-shade/)
This project introduces an original **risk indexing tool** that leverages scientific literature and incorporates new parameters developed through competition research. The tool is designed to categorize areas based on potential risk factors, particularly during future heat stress crises, with a focus on health and energy risk prediction.
The platform utilizes **geoTIFF data** pulled from a selected area within the Delhi metropolitan region using [ShadeMap](https://shademap.app/). Snapshots were taken every hour from 9 AM to 5 PM, and the fraction of shaded area was averaged across all time samples for each area. The data was then spatially binned (clustered by 8 pixels) and encoded as **geoJSON** to be displayed on the map.
This processing provides a **shade index** (ranging from 0 to 1) that indicates the amount of shade an area receives throughout the day, which is a crucial factor in predicting higher-risk areas during heat stress conditions.
## Features
![screenshot2.png](src/assets/screenshot2.png)
- **Interactive Map**: Map integrated with Mapbox.
- **Data Visualisation**: Markers with different colors for visual distinction.
## Technologies
- **Frontend**: Svelte
- **Map Integration**: [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
- **Build Tool**: Vite for fast development and optimized production builds.
## Getting Started
### Prerequisites
Ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v20+)
- npm or yarn
- A [Mapbox account](https://account.mapbox.com/) to get your access token.
### Installation
   
Install the dependencies:
   ```bash
   npm install
   ```
Create a `.env` file in the root directory and add your Mapbox access token:
   ```env
    VITE_MAPBOX_ACCESS_TOKEN=your-access-token
   ```
    
   
Start the development server:
   ```bash
   npm run dev
   ```
To build the project:
   ```bash
   npm run build
   ```


### Python environment


   ```bash
affine==2.4.0
anyio==4.3.0
appnope==0.1.4
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
arrow==1.3.0
asttokens==2.4.1
async-lru==2.0.4
attrs==23.2.0
Babel==2.15.0
beautifulsoup4==4.12.3
bleach==6.1.0
branca==0.8.0
certifi==2024.2.2
cffi==1.16.0
charset-normalizer==3.3.2
click==8.1.7
click-plugins==1.1.1
cligj==0.7.2
comm==0.2.2
contourpy==1.2.1
cycler==0.12.1
dateparser==1.2.0
debugpy==1.8.1
decorator==5.1.1
defusedxml==0.7.1
executing==2.0.1
fastjsonschema==2.19.1
folium==0.17.0
fonttools==4.53.0
fqdn==1.5.1
geojson==3.1.0
geopandas==1.0.1
h11==0.14.0
h3==3.7.7
httpcore==1.0.5
httpx==0.27.0
idna==3.7
ipykernel==6.29.4
ipython==8.24.0
ipywidgets==8.1.2
isoduration==20.11.0
jedi==0.19.1
Jinja2==3.1.4
json5==0.9.25
jsonpointer==2.4
jsonschema==4.22.0
jsonschema-specifications==2023.12.1
jupyter==1.0.0
jupyter-console==6.6.3
jupyter-events==0.10.0
jupyter-lsp==2.2.5
jupyter_client==8.6.1
jupyter_core==5.7.2
jupyter_server==2.14.0
jupyter_server_terminals==0.5.3
jupyterlab==4.1.8
jupyterlab_pygments==0.3.0
jupyterlab_server==2.27.1
jupyterlab_widgets==3.0.10
kiwisolver==1.4.5
MarkupSafe==2.1.5
matplotlib==3.9.0
matplotlib-inline==0.1.7
mistune==3.0.2
nbclient==0.10.0
nbconvert==7.16.4
nbformat==5.10.4
nest-asyncio==1.6.0
notebook==7.1.3
notebook_shim==0.2.4
numpy==1.26.4
overrides==7.7.0
packaging==24.0
pandas==2.2.2
pandocfilters==1.5.1
parso==0.8.4
pexpect==4.9.0
pillow==10.3.0
platformdirs==4.2.1
prometheus_client==0.20.0
prompt-toolkit==3.0.43
psutil==5.9.8
ptyprocess==0.7.0
pure-eval==0.2.2
pycparser==2.22
Pygments==2.18.0
pyogrio==0.10.0
pyparsing==3.1.2
pyproj==3.7.0
python-dateutil==2.9.0.post0
python-json-logger==2.0.7
pytz==2024.1
PyYAML==6.0.1
pyzmq==26.0.3
qtconsole==5.5.2
QtPy==2.4.1
rasterio==1.4.1
referencing==0.35.1
regex==2024.7.24
requests==2.31.0
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rpds-py==0.18.1
scipy==1.13.1
seaborn==0.13.2
Send2Trash==1.8.3
shapely==2.0.6
six==1.16.0
sniffio==1.3.1
soupsieve==2.5
stack-data==0.6.3
terminado==0.18.1
tinycss2==1.3.0
tornado==6.4
traitlets==5.14.3
types-python-dateutil==2.9.0.20240316
tzdata==2024.1
tzlocal==5.2
Unidecode==1.3.8
uri-template==1.3.0
urllib3==2.2.1
wcwidth==0.2.13
webcolors==1.13
webencodings==0.5.1
websocket-client==1.8.0
widgetsnbextension==4.0.10
word2number==1.1
xyzservices==2024.9.0

   ```

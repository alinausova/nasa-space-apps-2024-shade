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

    


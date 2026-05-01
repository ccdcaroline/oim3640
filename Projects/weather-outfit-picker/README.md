# Weather Outfit Picker (3 Progressive Sets)

This folder contains **three complete versions** of the same project, each one a progression:

1. `prototype`
2. `core-features`
3. `polished`

Each set has its own:

- `index.html`
- `styles.css`
- `script.js`

All sets fetch live weather from OpenWeather through a small local Node/Express API route, so your API key stays in `.env`.

## Folder structure

```text
weather-outfit-picker/
  prototype/
    index.html
    styles.css
    script.js
  core-features/
    index.html
    styles.css
    script.js
  polished/
    index.html
    styles.css
    script.js
  .env.example
  package.json
  server.js
```

## Setup in VS Code

1. Open this folder in VS Code.
2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file in this same folder:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
PORT=3000
```

You can copy `.env.example`.

## Run

```bash
npm start
```

Open any set in your browser:

- `http://localhost:3000/prototype`
- `http://localhost:3000/core-features`
- `http://localhost:3000/polished`

## Features checklist (all requested core features)

- Search for a city
- Fetch live weather data from OpenWeather
- Show temperature and weather condition
- Show outfit suggestion based on weather
- Show loading and error messages

## Progression summary

### 1) prototype

- Simplest UI
- Basic weather display
- Basic outfit suggestion logic

### 2) core-features

- Better layout and visual card design
- Weather icon + more details (feels like, humidity, wind)
- Unit toggle (C/F)
- Outfit shown as a checklist

### 3) polished

- Most refined look
- Dynamic themed background by weather
- Larger weather summary section
- More expressive outfit recommendation blocks

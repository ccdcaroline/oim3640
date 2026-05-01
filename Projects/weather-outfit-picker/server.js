const express = require("express");
const path = require("path");
const dotenv = require("dotenv");

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const WEATHER_API_KEY = process.env.OPENWEATHER_API_KEY;

const projectRoot = __dirname;

app.use("/prototype", express.static(path.join(projectRoot, "prototype")));
app.use("/core-features", express.static(path.join(projectRoot, "core-features")));
app.use("/polished", express.static(path.join(projectRoot, "polished")));

app.get("/", (req, res) => {
  res.type("html").send(`
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Weather Outfit Picker - Stages</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 2rem; background: #f5f7ff; color: #1f2a44; }
          .card { max-width: 700px; margin: 0 auto; background: #fff; border-radius: 14px; padding: 1.25rem 1.5rem; box-shadow: 0 10px 30px rgba(31,42,68,0.08); }
          h1 { margin-top: 0; }
          ul { line-height: 1.9; }
          a { color: #2855d9; text-decoration: none; font-weight: 600; }
          a:hover { text-decoration: underline; }
          code { background: #eef2ff; padding: 2px 6px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>Weather Outfit Picker</h1>
          <p>This project includes three progressive versions:</p>
          <ul>
            <li><a href="/prototype">Prototype</a></li>
            <li><a href="/core-features">Core Features</a></li>
            <li><a href="/polished">Polished</a></li>
          </ul>
          <p>Set your API key in <code>.env</code> as <code>OPENWEATHER_API_KEY=...</code>.</p>
        </div>
      </body>
    </html>
  `);
});

app.get("/api/weather", async (req, res) => {
  const city = req.query.city?.trim();
  const units = req.query.units === "imperial" ? "imperial" : "metric";

  if (!city) {
    return res.status(400).json({ error: "Please provide a city name." });
  }

  if (!WEATHER_API_KEY) {
    return res.status(500).json({
      error: "Missing OPENWEATHER_API_KEY in .env file.",
    });
  }

  const endpoint = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
    city
  )}&appid=${WEATHER_API_KEY}&units=${units}`;

  try {
    const response = await fetch(endpoint);
    const data = await response.json();

    if (!response.ok) {
      const message = data?.message || "Unable to fetch weather data.";
      return res.status(response.status).json({ error: message });
    }

    const temperatureC =
      units === "metric" ? data.main.temp : ((data.main.temp - 32) * 5) / 9;
    const temperatureF =
      units === "imperial" ? data.main.temp : (data.main.temp * 9) / 5 + 32;

    return res.json({
      city: data.name,
      country: data.sys?.country || "",
      tempC: Number(temperatureC.toFixed(1)),
      tempF: Number(temperatureF.toFixed(1)),
      feelsLikeC: Number(
        (
          units === "metric"
            ? data.main.feels_like
            : ((data.main.feels_like - 32) * 5) / 9
        ).toFixed(1)
      ),
      humidity: data.main.humidity,
      windKph: Number(((data.wind?.speed || 0) * 3.6).toFixed(1)),
      condition: data.weather?.[0]?.main || "Unknown",
      description: data.weather?.[0]?.description || "No description available",
      icon: data.weather?.[0]?.icon || "",
      weatherId: data.weather?.[0]?.id || null,
    });
  } catch (error) {
    return res.status(500).json({
      error: "Network error while contacting weather service.",
    });
  }
});

app.listen(PORT, () => {
  console.log(`Weather Outfit Picker running on http://localhost:${PORT}`);
});

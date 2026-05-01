const form = document.getElementById("weather-form");
const cityInput = document.getElementById("city-input");
const unitSelect = document.getElementById("unit-select");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const resultEl = document.getElementById("result");
const locationEl = document.getElementById("location");
const conditionEl = document.getElementById("condition");
const iconEl = document.getElementById("icon");
const tempEl = document.getElementById("temp");
const feelsLikeEl = document.getElementById("feels-like");
const humidityEl = document.getElementById("humidity");
const windEl = document.getElementById("wind");
const outfitListEl = document.getElementById("outfit-list");

function getOutfitItems(tempC, weatherId) {
  const rainy = weatherId >= 200 && weatherId < 600;
  const snowy = weatherId >= 600 && weatherId < 700;
  const items = [];

  if (tempC <= 3 || snowy) {
    items.push("Heavy coat", "Warm sweater", "Boots", "Gloves + scarf");
  } else if (tempC <= 10) {
    items.push("Jacket", "Long sleeve shirt", "Jeans", "Closed-toe shoes");
  } else if (tempC <= 18) {
    items.push("Light jacket/cardigan", "T-shirt", "Pants", "Sneakers");
  } else if (tempC <= 27) {
    items.push("T-shirt", "Shorts or light pants", "Breathable shoes");
  } else {
    items.push("Tank top or tee", "Shorts", "Light sneakers/sandals", "Water bottle");
  }

  if (rainy) {
    items.push("Umbrella or rain jacket");
  }

  return items;
}

function showLoading(isLoading) {
  loadingEl.classList.toggle("hidden", !isLoading);
  cityInput.disabled = isLoading;
  unitSelect.disabled = isLoading;
  form.querySelector("button").disabled = isLoading;
}

function showError(message = "") {
  errorEl.textContent = message;
  errorEl.classList.toggle("hidden", !message);
}

function renderOutfitList(items) {
  outfitListEl.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    outfitListEl.appendChild(li);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();
  const units = unitSelect.value === "imperial" ? "imperial" : "metric";

  if (!city) {
    showError("Please enter a city.");
    resultEl.classList.add("hidden");
    return;
  }

  showError("");
  showLoading(true);
  resultEl.classList.add("hidden");

  try {
    const response = await fetch(
      `/api/weather?city=${encodeURIComponent(city)}&units=${units}`
    );
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to fetch weather data.");
    }

    locationEl.textContent = `${data.city}${data.country ? `, ${data.country}` : ""}`;
    conditionEl.textContent = `${data.condition} - ${data.description}`;
    iconEl.src = data.icon ? `https://openweathermap.org/img/wn/${data.icon}@2x.png` : "";
    iconEl.alt = data.description ? `${data.description} icon` : "Weather icon";

    if (units === "imperial") {
      const tempCFromF = ((data.tempF - 32) * 5) / 9;
      tempEl.textContent = `${data.tempF}°F (${tempCFromF.toFixed(1)}°C)`;
      feelsLikeEl.textContent = `${data.feelsLikeC.toFixed(1)}°C`;
      renderOutfitList(getOutfitItems(tempCFromF, data.weatherId));
    } else {
      tempEl.textContent = `${data.tempC}°C (${data.tempF}°F)`;
      feelsLikeEl.textContent = `${data.feelsLikeC}°C`;
      renderOutfitList(getOutfitItems(data.tempC, data.weatherId));
    }

    humidityEl.textContent = `${data.humidity}%`;
    windEl.textContent = `${data.windKph} km/h`;
    resultEl.classList.remove("hidden");
  } catch (error) {
    showError(error.message || "Something went wrong.");
    resultEl.classList.add("hidden");
  } finally {
    showLoading(false);
  }
});

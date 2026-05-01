const form = document.getElementById("weather-form");
const cityInput = document.getElementById("city-input");
const submitBtn = document.getElementById("submit-btn");
const loadingEl = document.getElementById("loading-message");
const errorEl = document.getElementById("error-message");
const resultEl = document.getElementById("result");

const locationEl = document.getElementById("city");
const conditionEl = document.getElementById("description");
const weatherIcon = document.getElementById("weather-icon");
const tempEl = document.getElementById("temp");
const tempFEl = document.getElementById("temp-f");
const feelsLikeEl = document.getElementById("feels-like");
const humidityEl = document.getElementById("humidity");
const windEl = document.getElementById("wind");
const outfitTitleEl = document.getElementById("outfit-title");
const outfitAdviceEl = document.getElementById("outfit-body");
const checklistEl = document.getElementById("checklist");

function getOutfit(tempC, weatherId) {
  const rainy = weatherId >= 200 && weatherId < 600;
  const snowy = weatherId >= 600 && weatherId < 700;

  if (snowy || tempC <= 2) {
    return {
      title: "Deep Winter Bundle",
      advice:
        "Heavy coat, thermal top, scarf, gloves, and waterproof boots are your best option.",
      checklist: ["Heavy coat", "Thermal layer", "Gloves + scarf", "Waterproof boots"],
    };
  }
  if (tempC <= 10) {
    return {
      title: "Layered Comfort",
      advice: "Wear a jacket over a long-sleeve shirt with jeans and closed shoes.",
      checklist: ["Mid-weight jacket", "Long sleeves", "Jeans or pants", "Closed shoes"],
    };
  }
  if (tempC <= 20) {
    return {
      title: "Easy Everyday Fit",
      advice: "A t-shirt plus light jacket and pants keeps you comfortable all day.",
      checklist: ["T-shirt", "Light jacket", "Pants", "Sneakers"],
    };
  }
  if (rainy) {
    return {
      title: "Warm + Rain-Ready",
      advice: "Go with breathable clothing, but add a light rain jacket and water-resistant shoes.",
      checklist: ["Breathable top", "Light bottoms", "Rain jacket", "Water-resistant shoes"],
    };
  }
  if (tempC <= 28) {
    return {
      title: "Sunny Casual",
      advice: "T-shirt with shorts or light pants, plus comfortable sneakers.",
      checklist: ["T-shirt", "Shorts/light pants", "Sneakers", "Sunglasses"],
    };
  }
  return {
    title: "Hot Weather Plan",
    advice: "Choose lightweight breathable clothes, sunglasses, and keep water with you.",
    checklist: ["Light breathable top", "Shorts", "Sun protection", "Water bottle"],
  };
}

function setLoading(isLoading) {
  cityInput.disabled = isLoading;
  submitBtn.disabled = isLoading;
  loadingEl.classList.toggle("hidden", !isLoading);
}

function showError(message = "") {
  errorEl.textContent = message;
  errorEl.classList.toggle("hidden", !message);
}

function renderChecklist(items) {
  checklistEl.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    checklistEl.appendChild(li);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();

  if (!city) {
    showError("Please type a city name first.");
    resultEl.classList.add("hidden");
    return;
  }

  setLoading(true);
  showError("");
  resultEl.classList.add("hidden");

  try {
    const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}&units=metric`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not load weather data.");
    }

    const outfit = getOutfit(data.tempC, data.weatherId);
    locationEl.textContent = `${data.city}${data.country ? `, ${data.country}` : ""}`;
    conditionEl.textContent = `${data.condition} - ${data.description}`;
    tempEl.textContent = `${data.tempC.toFixed(1)}°C`;
    tempFEl.textContent = `(${data.tempF.toFixed(1)}°F)`;
    feelsLikeEl.textContent = `${data.feelsLikeC.toFixed(1)}°C`;
    humidityEl.textContent = `${data.humidity}%`;
    windEl.textContent = `${data.windKph} km/h`;

    weatherIcon.src = data.icon ? `https://openweathermap.org/img/wn/${data.icon}@2x.png` : "";
    weatherIcon.alt = `${data.description} icon`;

    outfitTitleEl.textContent = outfit.title;
    outfitAdviceEl.textContent = outfit.advice;
    renderChecklist(outfit.checklist);

    resultEl.classList.remove("hidden");
  } catch (error) {
    showError(error.message || "Something went wrong.");
    resultEl.classList.add("hidden");
  } finally {
    setLoading(false);
  }
});

const form = document.getElementById("weather-form");
const cityInput = document.getElementById("city-input");
const loadingMessage = document.getElementById("loading-message");
const errorMessage = document.getElementById("error-message");
const resultBox = document.getElementById("result");
const locationText = document.getElementById("location-text");
const tempText = document.getElementById("temp-text");
const conditionText = document.getElementById("condition-text");
const suggestionText = document.getElementById("suggestion-text");

function getOutfitSuggestion(tempC) {
  if (tempC < 5) {
    return "Wear a heavy coat, warm sweater, gloves, and boots.";
  }
  if (tempC < 13) {
    return "Layer up with a jacket, long sleeves, and jeans.";
  }
  if (tempC < 21) {
    return "A light sweater or hoodie with pants is a good choice.";
  }
  if (tempC < 28) {
    return "Try a t-shirt with shorts or light pants.";
  }
  return "It is hot - wear breathable clothes, sunglasses, and hydrate.";
}

function setLoadingState(isLoading) {
  cityInput.disabled = isLoading;
  form.querySelector("button").disabled = isLoading;
  loadingMessage.classList.toggle("hidden", !isLoading);
}

function showError(message = "") {
  errorMessage.textContent = message;
  errorMessage.classList.toggle("hidden", !message);
}

async function fetchWeather(city) {
  const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong.");
  }
  return data;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();

  if (!city) {
    showError("Please type a city first.");
    resultBox.classList.add("hidden");
    return;
  }

  setLoadingState(true);
  showError("");
  resultBox.classList.add("hidden");

  try {
    const weather = await fetchWeather(city);
    locationText.textContent = `${weather.city}, ${weather.country}`;
    tempText.textContent = `${weather.tempC}°C (${weather.tempF}°F)`;
    conditionText.textContent = weather.description;
    suggestionText.textContent = getOutfitSuggestion(weather.tempC);
    resultBox.classList.remove("hidden");
  } catch (error) {
    showError(error.message);
    resultBox.classList.add("hidden");
  } finally {
    setLoadingState(false);
  }
});

import React, { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
  // state to hold weather data
  const [weather, setWeather] = useState(null);

  // state to hold air quality data
  const [airQuality, setAirQuality] = useState(null);

  // state to hold PM10 forecast data
  const [pm10Forecast, setPm10Forecast] = useState([]);

  // state to hold PM10 historical data
  const [pm10Historical, setPm10Historical] = useState([]);

  useEffect(() => {
    // fetch current weather data
    axios
      .get("http://127.0.0.1:44933/weather/current/")
      .then((response) => setWeather(response.data))
      .catch((error) => console.error(error));

    // fetch current air quality data
    axios
      .get("http://127.0.0.1:44933/air/current/")
      .then((response) => setAirQuality(response.data))
      .catch((error) => console.error(error));

    // fetch PM10 forecast data
    axios
      .get("http://127.0.0.1:44933/air/predict/")
      .then((response) => setPm10Forecast(response.data))
      .catch((error) => console.error(error));

    // fetch PM10 historical data
    axios
      .get("http://127.0.0.1:44933/air/history/")
      .then((response) => setPm10Historical(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    
    <div className="App">
      <h1>Current Weather in Ptuj</h1>
      {weather ? (
        <div>
          <p>Temperature: {weather.temperature}</p>
          <p>Humidity: {weather.humidity}</p>
          <p>Wind: {weather.wind_speed}</p>
          <p>Pressure: {weather.pressure}</p>
        </div>
      ) : (
        <p>Loading weather data...</p>
      )}

      <h1>Current Air Quality in Ptuj</h1>
      {airQuality ? (
        <div>
          <p>PM10: {airQuality.pm10}</p>
        </div>
      ) : (
        <p>Loading air quality data...</p>
      )}

      <h1>PM10 Forecast for Ptuj</h1>
      {pm10Forecast.length > 0 ? (
        <div>
          {pm10Forecast.map((forecast, index) => (
            <div key={index}>
              <p>Date: {forecast.date}</p>
              <p>Value: {forecast.value}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading PM10 forecast data...</p>
      )}

      <h1>PM10 Historical Data for Ptuj</h1>
      {pm10Historical.length > 0 ? (
        <div>
          <ul>
            {pm10Historical.pm10_history.map((pm10, index) => (
              <li key={index}>{pm10}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Loading PM10 historical data...</p>
      )}
    </div>
  );
}


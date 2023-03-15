import React, { useState, useEffect } from "react";
import axios from "axios";
import './App.css';
import { FaTemperatureHigh, FaWind } from 'react-icons/fa';
import { WiHumidity } from 'react-icons/wi';
import { MdSearch } from 'react-icons/md';

export default function App() {
  // state to hold weather data
  const [weather, setWeather] = useState(null);

  // state to hold air quality data
  const [airQuality, setAirQuality] = useState(null);

  // state to hold PM10 forecast data
  const [pm10Forecast, setPm10Forecast] = useState([]);

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
  }, []);

  return (
    <div className="container">
      <header className="header">
        <h1 className="header__title">Weather App</h1>
        <form className="header__search">
          <input type="text" placeholder="Search location" />
          <button type="submit">
            <MdSearch />
          </button>
        </form>
      </header>
      <main>
        <div className="weather">
          <h2>Current Weather in Ptuj</h2>
          {weather ? (
            <div>
              <p>
                <FaTemperatureHigh /> {weather.temperature}°C
              </p>
              <p>
                <WiHumidity /> {weather.humidity}%
              </p>
              <p>
                <FaWind /> {weather.wind_speed} km/h
              </p>
            </div>
          ) : (
            <p>Loading weather data...</p>
          )}
        </div>
        <div className="air-quality">
          <h2>Air Quality Index (PM10)</h2>
          {airQuality ? (
            <div>
              <p className="air-quality__value">{airQuality.pm10}</p>
            </div>
          ) : (
            <p>Loading air quality data...</p>
          )}
        </div>
        <div className="forecast">
      <h2 className="forecast__title">PM10 Forecast</h2>
      <ul className="forecast__list">
        {pm10Forecast.map((item) => (
          <li key={item.date} className="forecast__item">
            <p className="forecast__item-date">{item.date}</p>
            <p className="forecast__item-value">{item.value}</p>
          </li>
        ))}
      </ul>
    </div>
      </main>
    </div>
  )};
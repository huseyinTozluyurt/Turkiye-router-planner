import { useEffect, useState } from 'react';
import './App.css';
import MapView from './MapView';

function App() {
  const [cities, setCities] = useState([]);
  const [coordinates, setCoordinates] = useState({});
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [visitCount, setVisitCount] = useState(0);
  const [visitCities, setVisitCities] = useState([]);
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/cities")
      .then(res => res.json())
      .then(setCities);

    fetch("http://localhost:5000/city-coordinates")
      .then(res => res.json())
      .then(setCoordinates);
  }, []);

  const handleSubmit = async () => {
    const response = await fetch("http://localhost:5000/shortest-path", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start, end, mustVisit: visitCities })
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div id="root">
      <div className="left-panel">
        <div className="container">
          <h1>Türkiye Shortest Route Planner</h1>

          <label>Start City:</label>
          <select value={start} onChange={e => setStart(e.target.value)}>
            <option value="">Select</option>
            {cities.map(city => <option key={city}>{city}</option>)}
          </select>

          <label>End City:</label>
          <select value={end} onChange={e => setEnd(e.target.value)}>
            <option value="">Select</option>
            {cities.map(city => <option key={city}>{city}</option>)}
          </select>

          <label>How many cities to visit?</label>
          <input
            type="number"
            value={visitCount}
            onChange={e => {
              const count = Number(e.target.value);
              setVisitCount(count);
              setVisitCities(Array(count).fill(""));
            }}
          />

          {visitCities.map((_, i) => (
            <div key={i}>
              <label>City {i + 1}:</label>
              <select
                value={visitCities[i]}
                onChange={e => {
                  const updated = [...visitCities];
                  updated[i] = e.target.value;
                  setVisitCities(updated);
                }}
              >
                <option value="">Select</option>
                {cities.map(city => <option key={city}>{city}</option>)}
              </select>
            </div>
          ))}

          <button onClick={handleSubmit}>Calculate Shortest Path</button>

          {result?.path && (
            <div className="result">
              <h2>📍 Shortest Route</h2>
              <p>{result.path.join(" → ")}</p>
              <p>📏 Total Distance: {result.distance} km</p>
            </div>
          )}

          {result?.error && <p className="error">{result.error}</p>}
        </div>
      </div>

      <div className="right-panel">
        {result?.path && coordinates && (
          <MapView path={result.path} coordinates={coordinates} />
        )}
      </div>
    </div>
  );
}

export default App;

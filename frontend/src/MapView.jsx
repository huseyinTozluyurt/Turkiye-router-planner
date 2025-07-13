import React from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapView = ({ path, coordinates }) => {
  if (!path || path.length < 2 || Object.keys(coordinates).length === 0) return null;

  const toKey = (city) => city.toUpperCase('tr');  // Turkish case-sensitive normalization

  const routeCoords = path.map(city => {
    const key = toKey(city);
    const coord = coordinates[key];
    if (!coord) console.warn("Missing coordinate for:", key);
    return coord ? [coord[0], coord[1]] : null;
  }).filter(Boolean);

  return (
    <MapContainer center={[39.0, 35.0]} zoom={6} scrollWheelZoom={true} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      />

      <Polyline positions={routeCoords} color="blue" weight={4} />

      {routeCoords.map(([lat, lon], index) => (
        <Marker key={index} position={[lat, lon]}>
          <Popup>{`${index + 1}. ${path[index]}`}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapView;

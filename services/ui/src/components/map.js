import React, { useState } from 'react';
import { YMaps, Map, Placemark } from '@pbe/react-yandex-maps';

const MarkersMap = (params) => {
  const [mapCenter, setMapCenter] = useState([55.75, 37.57]);

  const [loading, setLoading] = useState(true);
  
  const [error, setError] = useState(false);
  let markers;
  
  if (params.markers) {
    markers = params.markers.map(url => [url.lat, url.lng]);
  } else {
    setError(true);
  }

  return ( 
    <div>
    {loading && (
        <p>... Loading video stream locations on map...</p>
      )}
    {error && (
        <p>Error: unable to load markers data.</p>
      )}
      
    <YMaps>
      <Map  width="100%" height="500px" onLoad={() => {
        setLoading(false);}}
        
        defaultState={{ center: mapCenter, zoom: 3 }}
        onBoundsChange={({ target }) => target && setMapCenter(target.getCenter())}>
        {markers.map((coords, index) => (
          <Placemark
            key={index}
            geometry={coords}
            options={{ preset: 'islands#blueCircleDotIcon' }}
          />
        ))}
      </Map>

  </YMaps>
  </div>
);};

export default MarkersMap;

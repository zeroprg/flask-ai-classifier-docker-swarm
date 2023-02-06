import React, { useState } from 'react';
import { YMaps, Map, Placemark, ZoomControl, FullscreenControl } from '@pbe/react-yandex-maps';

const MarkersMap = (params) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  let markers; 
  let cams;


  if (params.markers) {
    markers = params.markers.map(url => [url.lat, url.lng]);
    cams = params.markers.map(url => url.cam);
  } else {
    setError(true);
  }

  const handleMarkerClick = (cam) => {
    const stream = document.getElementById(`stream${cam}`);
    const div= document.getElementById(cam);
     
    if (stream) {
      stream.scrollIntoView({ behavior: 'smooth' });
      stream.focus();
      div.style.boxShadow = " 0 0 10px 5px green";
    }
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
        <Map width="100%" height="400px" onLoad={() => { setLoading(false); }}
          defaultState={{ center: [55.75, 37.57], zoom: 3 }}
        >
          {markers.map((coords, index) => (
            <Placemark
              key={index}
              geometry={coords}
              options={{ preset: 'islands#blueCircleDotIcon' }}
              onClick={() => handleMarkerClick(cams[index])}
            />
          ))}
          <ZoomControl options={{ float: "right" }} />
          <FullscreenControl />
        </Map>

      </YMaps>
    </div>
  );
};

export default MarkersMap;

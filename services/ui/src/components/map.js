import React, { useState } from 'react';
import { YMaps, Map, Placemark } from '@pbe/react-yandex-maps';

const MarkersMap = (params) => {
  const [mapCenter, setMapCenter] = useState([55.75, 37.57]);
  //const urls = [ {lat:51.2 , lng: -112.1} , {lat:51.3  , lng: -115.2} ];
  const [markers, setMarkers] = useState( params.markers.map(url => [url.lat, url.lng]));
  const [loading, setLoading] = useState(true);
  const mapStyles = {
    width: '100%',
    height: '100%'
  };
  
  return (
    <div>
    {loading && (
        <p>... Loading video stream locations on map...</p>
      )}
      
    <YMaps>
      <Map  width="100%" height="200px" onLoad={() => {
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

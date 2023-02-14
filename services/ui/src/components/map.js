import React, { useState } from 'react';
import { YMaps, Map, Placemark, ZoomControl, FullscreenControl } from '@pbe/react-yandex-maps';

const MarkersMap = ({markers}) => {
  const [loading, setLoading] = useState(true);
  const is_counted = (count) =>{
    return count > 0 ? 'Founded '+count+ ' objects per 1000 frames<br/>': '';
  }

  const handleMarkerClick = (cam) => {
    const stream = document.getElementById(`stream${cam}`);
    const div= document.getElementById(cam);
     
    if (stream) {
      stream.scrollIntoView({ behavior: 'smooth' });
      stream.focus();
      div.style.boxShadow = " 0 0 10px 5px blue";
    }
  }

  return (
    <div>
      {loading && (
        <p>... Loading video stream locations on map...</p>
      )}


      <YMaps>
        <Map width="100%" height="350px" onLoad={() => { setLoading(false); }}
          defaultState={{ center: [55.75, 37.57], zoom: 3 }}
          
        >
          {markers.map((url) => (
            <Placemark
              key={url.cam}
              geometry={[url.lat, url.lng]}
              modules={['geoObject.addon.balloon']}            
              onClick={() => handleMarkerClick(url.cam)}

              properties={{
                balloonContentHeader: '',
                balloonContentBody: `${url.city}:<br/>${is_counted(url.objects_counted)}Idle in mins: ${url.idle_in_mins}<br/>`,
                balloonContentFooter: '',
                iconContent: `${url.city}, ${url.country}, ${url.postalcode}`,
              }}
              options={{
                preset: 'islands#yellowStretchyIcon',
                iconColor: 'green',
                openHintOnHover: true,
              }}
            >

            </Placemark>
          ))}
          <ZoomControl options={{ float: "right" }} />
          <FullscreenControl />
        </Map>

      </YMaps>
    </div>
  );
};

export default MarkersMap;

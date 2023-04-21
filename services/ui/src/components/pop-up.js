import React, { useEffect, useState } from "react";
import axios from 'axios'

function Popup(props) {
  
  const [isLoading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const loadData = () => {
    const DEFAULT_QUERY = global.config.API + 'health';
    setLoading(true);
  
    axios
      .get(DEFAULT_QUERY)
      .then(response => {
        if (response.status === 200) {
          setLoading(false);
          return response.data;
        } else {
          console.log('error:');
          throw new Error('Something went wrong ...');
        }
      })
      .then(data => {
        setLoading(false);
        setData(data);       
      })
      .catch(error => setLoading(false));
  };
 


  // Set a timer to close the modal after 10 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      props.onClose();
    }, 15000);

    loadData();

    // Clear the timer if the component unmounts or if onClose changes
    return () => clearTimeout(timer);
  }, []);

  return  (
    <div className="popup">
      <div className="popup-inner">
        <div className="popup-header">
          
          <button className="close-button" onClick={props.onClose}>X</button>
        </div>
        <div className="popup-content">
          {data ? (
            <>
              <p style={{ color: '#07ff7f' }}>Total: <b>{data.objects}</b> objects from <b >{data.cams}</b> cams</p>
              <p style={{ color: '#07ff7f' }}>Last hour:  <b>{data.last_hour_persons} persons founded</b> </p>
              <p style={{ color: '#07ff7f' }}>Total: <b>{data.nodes}</b> processes work on <b>{data.videostreams}</b> videostreams:</p>
            </>
          ): (<img alt ="" src={'img/fancybox_loading.gif'}></img>)}
        </div>
      </div>
    </div>
  );
}

export default Popup;

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
          {data &&  (
            <>
              <p>Total {data.objects} objects from {data.cams} cams</p>
              <p>Last hour: {data.last_hour_persons} persons founded </p>
              <p>Total {data.nodes} processes work on {data.videostreams} videostreams:</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Popup;

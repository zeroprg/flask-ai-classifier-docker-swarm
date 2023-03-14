import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const ObjectOfInterest = (props) => {
  const loadStyle = {
    height: '150px'
  };
  const tabcontentStyle = {
    width: window.innerWidth-20,
    textAlign: 'center'
  };

  const popup_image = (event) =>{
    if(event.target.classList.contains('img_thumb')){
      event.target.classList.replace('img_thumb', 'popup');   
    } else if(event.target.classList.contains('popup')){
      event.target.classList.remove('popup', 'img_thumb');    
    }
  };

  const [data, setData] = useState(props.data);
  const [loading, setLoading] = useState(true);

  const dataCacheRef = useRef({});

  function fetchData(cam, timerange) {
    const DEFAULT_QUERY = global.config.API + "moreimgs";
    const query = new URL(DEFAULT_QUERY);

    if (timerange) {
      query.searchParams.append('hour_back1', timerange.start);
      query.searchParams.append('hour_back2', timerange.end);
    }

    query.searchParams.append('cam', cam);
    setLoading(true);

    // Check cache first
    if (dataCacheRef.current[query.toString()]) {
      setData(dataCacheRef.current[query.toString()]);
      setLoading(false);
      return;
    }

    axios.get(query.toString())
      .then(response => {
        if (response.status === 200) {
          setData(response.data);
          dataCacheRef.current[query.toString()] = response.data; // Store in cache
        } else {
          console.log("error when connect to :" + DEFAULT_QUERY);
        }
      })
      .catch(error => {
        console.log(error);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  const prevTimerangeRef = useRef(null);

  useEffect(() => {
    fetchData(props.cam, prevTimerangeRef.current);
  }, [props.cam]);

  useEffect(() => {
    if (prevTimerangeRef.current && !(prevTimerangeRef.current.end === props.timerange.end && prevTimerangeRef.current.start === props.timerange.start) ) {
      fetchData(props.cam, props.timerange);
    }
    prevTimerangeRef.current = props.timerange;
  }, [props.cam, props.timerange]);

  useEffect(() => {
    if (props.data) {
      setData(props.data);
      setLoading(false);
    }
  }, [props.data]);


  if ( loading ) {
    return ( 
      <div style={tabcontentStyle}> 
        <img alt="" src={'img/fancybox_loading@2x.gif'} style={loadStyle}/>
      </div>
    );
  }

  return (       
    <React.Fragment>
     {
     (data &&  data.length > 0) ?
      <div id={'Objectsfilter'+ props.cam } style={{display:'block'}}>
        <div id={'cam'+ props.cam} className="images_row">
          {data.map(data =>
            <img key={data.hashcode} id={data.hashcode} className={'img_thumb'} src={data.frame}  alt={data.currentime} onClick={popup_image.bind(this)} />
          )} 
        </div> 
      </div> 
      : ( <div style={tabcontentStyle}><h1> No Data </h1></div>)
      }
    </React.Fragment>                        
  );
};

export default ObjectOfInterest;

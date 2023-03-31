import React, { useState } from 'react';
import { Tabs, Tab } from 'react-bootstrap';

import ObjectOfInterestPlot from './obj_plot'
import ObjectOfInterest from './objects_of_interest'
import axios from 'axios'
import Video from './video';

const VideoStreamer = ({ camera, showVideoSectionOnly, showvideosection, showMaxResolution, maxResolution, child, timerange, object_of_interest }) => {

  const [localTimerange, setLocalTimerange] = useState(timerange);
  const [localObjectOfInterest, setLocalObjectOfInterest] = useState(object_of_interest);
  const [isShown, setIsShown] = useState(false);
  const [data, setData] = useState(null);

  const handleHashcodes = (dataFromPlotter) => {
    const clickedValues = dataFromPlotter.hashcodes; 
    const clickedValuesStr = clickedValues.substring(1, clickedValues.length - 1).replace(/'/g, '');
    const queryString = "?hashcodes="+clickedValuesStr;
    // do something with the clicked value
    axios.get(global.config.API + "moreimgs" + queryString)
      .then(response => {
        //console.log(response.data);
        setData(response.data);
      })
      .catch(error => {
        console.log(error);
      });
    
  }

  const onTimeChanged = (timerange) => {
    setLocalTimerange(timerange);
  };

  const onParamsChanged = (object_of_interest) => {
    setLocalObjectOfInterest(object_of_interest);
  };



  return (
    <section id={'section' + camera.cam} key={'section' + camera.cam} style={{ display: 'block' }}>
      <div className="row"
        onMouseEnter={() => setIsShown(true)}
        onMouseLeave={() => setIsShown(false)}>
        <div className="col-sm-12">
          {child}
          <Video key={camera.id} camera={camera} showBoxes={false}
            showVideoSectionOnly={showVideoSectionOnly}
            showvideosection={showvideosection}
            showMaxResolution={showMaxResolution}
            maxResolution={maxResolution} />
        </div>
        <div className="col-sm-12">
          <ObjectOfInterestPlot cam={camera.id}
            timerange={localTimerange}
            onParamsChanged={onParamsChanged}
            onTimeChanged={onTimeChanged}
            onBarClick={handleHashcodes}
            object_of_interest={object_of_interest} />
        </div>
      </div>
      <div className="row">
        <div className="col-sm-12">
          <Tabs defaultActiveKey="founded_objects" id="uncontrolled-tab">
            <Tab eventKey="founded_objects" title="Founded Objects" className="tabcontent">
              <ObjectOfInterest object_of_interest={localObjectOfInterest}
                data={data}
                timerange={localTimerange}
                cam={camera.id} />
            </Tab>
          </Tabs>
        </div>
      </div>
    </section>
  );
};

export default VideoStreamer;

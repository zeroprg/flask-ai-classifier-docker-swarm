import React, { useState } from 'react';
import { Tabs, Tab } from 'react-bootstrap';

import ObjectOfInterestPlot from './obj_plot'
import ObjectOfInterest from './objects_of_interest'
import Video from './video';

const VideoStreamer = ({ camera, showVideoSectionOnly, showvideosection, showMaxResolution, maxResolution, child, timerange, object_of_interest }) => {

  const [localTimerange, setLocalTimerange] = useState(timerange);
  const [localObjectOfInterest, setLocalObjectOfInterest] = useState(object_of_interest);
  const [isShown, setIsShown] = useState(false);

  const onTimeChanged = (timerange) => {
    setLocalTimerange(timerange);
  };

  const onParamsChanged = (object_of_interest) => {
    setLocalObjectOfInterest(object_of_interest);
  };

  const well = isShown ? { boxShadow: " 0 0 10px 5px green" } : {};

  return (
    <section id={'section' + camera.cam} key={'section' + camera.cam} style={{ display: 'block' }}>
      <div className="row" style={well}
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
            object_of_interest={object_of_interest} />
        </div>
      </div>
      <div className="row">
        <div className="col-sm-12">
          <Tabs defaultActiveKey="founded_objects" id="uncontrolled-tab">
            <Tab eventKey="founded_objects" title="Founded Objects" className="tabcontent">
              <ObjectOfInterest object_of_interest={localObjectOfInterest}
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

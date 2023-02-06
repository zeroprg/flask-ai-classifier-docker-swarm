import React ,{ useState} from 'react';

import VideoStreamer from './video-streamer';
import Video from './video';
import Media from 'react-media';
import { Fragment } from 'react';

const VideoStat  = ({camera, timerange, object_of_interest}) => {
    const [showvideosection, setShowVideosection] = useState(true);
    const [maxResolution, setMaxResolution] = useState(false);

    const videoClickHandlerEvent = () => {
        setShowVideosection(!showvideosection);
    };

    const maxResolutionClickHandlerEvent = () => {
        setMaxResolution(!maxResolution);
    };

    const showVideoSectionOnly = (showvideosection, classname, camera) => (
        showvideosection ?

            <div key={`cam${camera.cam}`} className={classname}>            
                <Video camera={camera} 
                  showVideoSectionOnly={videoClickHandlerEvent} 
                  showVideoSection = {showvideosection}                 
                  showMaxResolution = {maxResolutionClickHandlerEvent}
                  maxResolution = {maxResolution} 
                  />
            </div>
            :             
            <VideoStreamer key={camera.url}
                    camera={camera}
                    timerange={timerange}
                    object_of_interest={object_of_interest}
                    showVideoSectionOnly={videoClickHandlerEvent} 
                    showVideoSection = {showvideosection}                 
                    showMaxResolution = {maxResolutionClickHandlerEvent}
                    maxResolution = {maxResolution}                   
            />         
    );

    return (
        <Media queries={{
                        small: "(max-width: 500px)",
                        medium: "(min-width: 600px) and (max-width: 1366px)",
                        large: "(min-width: 1367px)"
                        }}>
                        {matches => {
                                return (
                                    <Fragment>
                                        {matches.small &&
                                                showVideoSectionOnly(showvideosection, "col-sm-12", camera)}
                                        {matches.medium &&
                                                showVideoSectionOnly(showvideosection, maxResolution? "col-sm-12": "col-sm-6", camera)}
                                        {matches.large &&
                                                showVideoSectionOnly(showvideosection, maxResolution? "col-sm-12": "col-sm-4", camera)}
                                    </Fragment>

                                );
                        }}
        </Media>
    

    );
}

export default VideoStat;
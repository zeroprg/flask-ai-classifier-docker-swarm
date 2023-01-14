import React ,{ useEffect, useState} from 'react';

import VideoStreamer from './video-streamer';
import Video from './video';
import Media from 'react-media';
import { Fragment } from 'react';

const VideoStat  = ({camera, timerange, object_of_interest}) => {
    const [showvideosection, setShowVideoSectionOnly] = useState(true);

    const videoClickHandler = () => (
        setShowVideoSectionOnly(!showvideosection)
    );


    const showVideoSectionOnly = (showvideosection, classname, camera) => (
        showvideosection ?
            <div key={`cam${camera.cam}`} className={classname}>            
                <Video camera={camera} showVideoSectionOnly={videoClickHandler} />
            </div>
            :             
            <VideoStreamer key={camera.url}
                    camera={camera}
                    timerange={timerange}
                    object_of_interest={object_of_interest}
                    showVideoSectionOnly={videoClickHandler}     
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
                                                showVideoSectionOnly(showvideosection, "col-sm-6", camera)}
                                        {matches.large &&
                                                showVideoSectionOnly(showvideosection, "col-sm-4", camera)}
                                    </Fragment>

                                );
                        }}
        </Media>
    

    );
}

export default VideoStat;
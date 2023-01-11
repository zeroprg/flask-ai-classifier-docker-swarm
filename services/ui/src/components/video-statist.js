import React ,{ useEffect, useState} from 'react';

import VideoStreamer from './video-streamer';
import Video from './video';
import Media from 'react-media';
import { Fragment } from 'react';

const VideoStat  = ({camera, timerange, object_of_interest}) => {
    const [showvideo, setShowVideo] = useState(true);
    const [current, setClass] = useState("fa fa-bar-chart");

    const videoClickHandler = () => (
        setShowVideo(!showvideo)
        //setClass(showvideo? "fa fa-bar-chart" : "fa fa-play")
    );

    const menu = () => (
        <nav className="menu">
            <input type="checkbox" href="#" className="menu-open" name="menu-open" id="menu-open"/>
            <label className="menu-open-button" htmlFor="menu-open">
                <span className="hamburger hamburger-1"></span>
                <span className="hamburger hamburger-2"></span>
                <span className="hamburger hamburger-3"></span>
            </label>            
            <a href="#" className="menu-item"> <i className="fa fa-bar-chart"></i> </a>    
        </nav>
    );
    const showVideoSection = (showvideo, classname, camera) => (
        showvideo ?
            <div key={`cam${camera.cam}`} className={classname}>
                {menu()}
                <Video camera={camera} />
            </div>
            :
            <VideoStreamer key={camera.url}
                camera={camera}
                timerange={timerange}
                object_of_interest={object_of_interest}
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
                                                showVideoSection(showvideo, "col-sm-12", camera)}
                                        {matches.medium &&
                                                showVideoSection(showvideo, "col-sm-6", camera)}
                                        {matches.large &&
                                                showVideoSection(showvideo, "col-sm-4", camera)}
                                    </Fragment>

                                );
                        }}
        </Media>
    

    );
}

export default VideoStat;
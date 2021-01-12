import React ,{ useEffect, useState} from 'react';
import { Menu, Item } from "react-gooey-nav";
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
    
    const menu = (showStatistic) => (<Menu> 
        <Item title="Twitter!"> <i className = {"fa fa-twitter"}/></Item>
    {/*    <Item title="Facebook!"  component="a"
              componentProps={{
                    href: "https://facebook.com",
                    target: "_blank",
                    rel: "noopener",
                    onClick: (e) => {   
                   // console.log("Facebook button clicked");
                    e.preventDefault();
                    }
                }}>
        
         <i className={"fa fa-facebook"}/>
        </Item>
        */}
        <Item title={showStatistic?"Show statistic":"back to Video"} component="a" 
              componentProps={{ onClick: (e) => {     
                  e.preventDefault();                                  
                  videoClickHandler();} }}> 
          <i className= {showStatistic?"fa fa-bar-chart":"fa fa-play"}/>
        </Item>
    </Menu>
    );
    const showVideoSection = (showvideo, classname, camera) => (
        showvideo ?
            <div key={`cam${camera.cam}`} className={classname}>
                {menu(showvideo)}
                <Video camera={camera} />
            </div>
            :
            <VideoStreamer key={camera.url}
                camera={camera}
                timerange={timerange} 
                object_of_interest={object_of_interest}
                child= {menu(showvideo)}/>
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
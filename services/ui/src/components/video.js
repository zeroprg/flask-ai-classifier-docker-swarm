import React ,{ useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { propTypes } from 'react-bootstrap/esm/Image';
//import { useMediaQuery } from 'react-responsive';


const Video = ({camera, showBoxesAroundObjects, showVideoSectionOnly}) => {
    const HOST = global.config.API
    //let checkBoxElem = useRef(null)    
    const [showBoxes, setShowBoxes] = useState(showBoxesAroundObjects);
    //const isMobile = useMediaQuery({ query: '(max-width: 600px)' });
    const useStyles = makeStyles({
        root: {
            '-webkit-user-select': 'none',
             display: 'block',
             width: '100%',
             'min-width':'200px',
             height: 'auto',             
             'padding-top': '5px',
             'padding-bottom': '5px',
        },
      });
      const classes = useStyles(); 

    const [showvideo, setShowVideo] = useState(true);
    const [isShown, setIsShown] = useState(false);
    
    const videoClickHandler = () => {
        setShowVideo(!showvideo);
    };
    
    
    const menu = (isShown, showvideo) => (
        isShown ?
        <nav className="menu">
            <input type="checkbox" href="#" className="menu-open" name="menu-open" id="menu-open"/>
            <label className="menu-open-button" htmlFor="menu-open" >
                <span className="hamburger hamburger-1"></span>
                <span className="hamburger hamburger-2"></span>
                <span className="hamburger hamburger-3"></span>
            </label>            
            <span  className="menu-item" onClick={()=>{ videoClickHandler(); showVideoSectionOnly();}}> 
                <i className={ showvideo ? "fa fa-bar-chart" : "fa fa-play"}></i>
            </span>            
        </nav>
        :<span/>
    );
           

// <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button>             <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button></b>         <br/> 

    const changeCheckBoxInput = () => {
            setShowBoxes(!showBoxes)
        }


    useEffect(() => {
        setShowBoxes(showBoxes);

        }, [showBoxes]);

        //style={{padding-top:'100px;'}}
        //                <input type="checkbox" class="custom-control-input" id={"checked"+ camera.id} 
//                       onChange={changeCheckBoxInput}/> 
//                <label class="custom-control-label" htmlFor={"checked"+ camera.id}> Show catched objects for {camera.url}</label>

    return(<span      
            onMouseEnter={() => setIsShown(true)}
            onMouseLeave={() => setIsShown(false)}  >
            {menu(isShown,showvideo)}

            <div style={{paddingTop:20}} ></div>
            <img id={'stream'+camera.cam}  className={classes.root}
                 src={ showBoxes ? HOST+"video_feed?cam="+camera.id : camera.url } 
                 alt="Video Streamer"
                 

                 >
    
            </img>    

            </span>
  );
}
export default Video
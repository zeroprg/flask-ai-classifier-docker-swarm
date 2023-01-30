import React ,{ useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';

const Video = ({camera, showBoxesAroundObjects, showVideoSectionOnly, showvideosection, showMaxResolution, maxResolution}) => {
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

    const [isShown, setIsShown] = useState(false);
    


    
    
    const menu = (isShown, showvideosection, maxResolution) => (
        isShown ?
        <nav className="menu">
            <input type="checkbox" href="#" className="menu-open" name="menu-open" id="menu-open"/>
            <label className="menu-open-button" htmlFor="menu-open" >
                <span className="hamburger hamburger-1"></span>
                <span className="hamburger hamburger-2"></span>
                <span className="hamburger hamburger-3"></span>
            </label>            
            <span  className="menu-item" onClick={()=>{ showVideoSectionOnly();}}> 
                <i className={ !showvideosection ? "fa fa-bar-chart" : "fa fa-play"}></i>
            </span>
            <span  className="menu-item" onClick={()=>{showVideoSectionOnly(); showMaxResolution();}}> 
                <i className={ !maxResolution ? "fa fa-expand" : "fa fa-toggle-down"}></i>
            </span>            
        </nav>
        :<span/>
    );
           

// <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button>             <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button></b>         <br/> 

    const changeCheckBoxInput = () => {
            setShowBoxes(!showBoxes)
    }
    const well= isShown ? {
        boxShadow: " 0 0 10px 5px green"
    }
    : {}


    useEffect(() => {
        setShowBoxes(showBoxes);

        }, [showBoxes]);

        //style={{padding-top:'100px;'}}
        //                <input type="checkbox" class="custom-control-input" id={"checked"+ camera.id} 
//                       onChange={changeCheckBoxInput}/> 
//                <label class="custom-control-label" htmlFor={"checked"+ camera.id}> Show catched objects for {camera.url}</label>

    return(<div style={well}     
            onMouseEnter={() => setIsShown(true)}
            onMouseLeave={() => setIsShown(false)}>
            {menu(isShown, showvideosection, maxResolution)}

         
            <img id={'stream'+camera.cam}  className={classes.root}
                 src={ showBoxes ? HOST+"video_feed?cam="+camera.id : camera.url } 
                 alt="Video Streamer">
    
            </img>    

            </div>
  );
}
export default Video
import React ,{ useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { SnackbarConsumer } from '../snackbarContext';

import axios from 'axios'


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
    const scrollToCamera = ()=>{
        const stream = document.getElementById(`stream${camera.cam}`);
        const div= document.getElementById(camera.cam);
          stream.scrollIntoView({ behavior: 'smooth' });
          stream.focus();
          div.style.boxShadow = " 0 0 10px 5px green";
    } 
    const activateCamera = (handleOpen) => {
        const URL = HOST + "urls"
        const payload = {
            id: camera.id,
            url: camera.url,
            objects_counted: 0 // activate this camera
        }
        axios.put(URL, payload)
            .then(function (response) {
                console.log(response);
                handleOpen(response.data.message, 'success')
            })
            .catch(function (error) {
                console.log(error);
                handleOpen(error.response.data.message, 'error')
            });
    }
    
    
    const menu = (isShown, showvideosection, maxResolution) => (
        isShown ?
        <nav className="menu">
            <input type="checkbox" href="#" className="menu-open" name="menu-open" id="menu-open"/>
            <label className="menu-open-button" htmlFor="menu-open" >
                <span className="hamburger hamburger-1"></span>
                <span className="hamburger hamburger-2"></span>
                <span className="hamburger hamburger-3"></span>
                <span className="hamburger hamburger-4"></span>
            </label>            

            <span  className="menu-item" onClick={()=>{ showMaxResolution();}}> 
                <i className={ !maxResolution ? "fa fa-expand" : "fa fa-toggle-down"}></i>
            </span>
            {
            camera.objects_counted < 0 ? 
            <SnackbarConsumer>
                {({ handleOpen}) => (  
                <span  className="menu-item" onClick={()=>{activateCamera(handleOpen)}}> 
                    <i className="fa fa-camera"></i>
                </span>
                )}
            </SnackbarConsumer>
            : 
            <span  className="menu-item" onClick={()=>{ showVideoSectionOnly();}}> 
                <i className={ !showvideosection ? "fa fa-bar-chart" : "fa fa-play"} onClick={()=>{scrollToCamera()}}></i>
            </span>         
            }  
            <SnackbarConsumer>            
                {({handleMapPoint}) => ( 
                <span  className="menu-item" onClick={()=>{handleMapPoint([camera.lat,camera.lng])}}> 
                    <i className="fa fa-map"></i>
                </span>
                )}
            </SnackbarConsumer>           
            
        </nav>
        :<span/>
    );
           

// <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button>             <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button></b>         <br/> 


    const well= isShown ? {
        boxShadow: " 0 0 10px 5px green"
    }
    : {}
    const header = (camera.city?camera.city+',':'') + (camera.region?camera.region+',':'') + (camera.country?camera.country:'')

    useEffect(() => {
        setShowBoxes(showBoxes);

        }, [showBoxes]);

        //style={{padding-top:'100px;'}}
        //                <input type="checkbox" class="custom-control-input" id={"checked"+ camera.id} 
//                       onChange={changeCheckBoxInput}/> 
//                <label class="custom-control-label" htmlFor={"checked"+ camera.id}> Show catched objects for {camera.url}</label>

    return(<div id={camera.cam} style={well}     
            onMouseEnter={() => setIsShown(true)}
            onMouseLeave={() => setIsShown(false)}>
            {menu(isShown, showvideosection, maxResolution)}

            <p>{header}</p>
            <img id={'stream'+camera.cam}  className={classes.root} alt={header}
                 src={ showBoxes ? HOST+"video_feed?cam="+camera.id : camera.url }>
    
            </img>    

            </div>
  );
}
export default Video
import React ,{ useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
//import { useMediaQuery } from 'react-responsive';



const Video = ({camera, showBoxesAroundObjects}) => {
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


// <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button>             <b> {camera.url}: <button id={'drwZone'+ camera.cam} onClick = {this.showframes? 'refresh(' + camera.cam +')'}>Show zones</button></b>         <br/> 

    const changeCheckBoxInput = () => {
            setShowBoxes(!showBoxes)
        }


    useEffect(() => {
        setShowBoxes(showBoxes);
        }, [showBoxes]);

        //style={{padding-top:'100px;'}}
    return(<span>
            <div class="custom-control custom-checkbox" style={{paddingTop:'100px;'}} >
                <input type="checkbox" class="custom-control-input" id={"checked"+ camera.cam} 
                       onChange={changeCheckBoxInput}/> 
                <label class="custom-control-label" for={"checked"+ camera.cam}> Show catched objects for {camera.url}</label>
               
            </div>
            <img id={'stream'+camera.cam}  className={classes.root}
                 src={ showBoxes ? HOST+"video_feed?cam="+camera.cam : camera.url } 
                 alt="Video Streamer"/>
            </span>
  );
}
export default Video
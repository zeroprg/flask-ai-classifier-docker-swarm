import React, { useState, useRef, useEffect } from 'react';
import { SnackbarProvider } from './snackbarContext';

import URLlist from './components/urls'
import InputURL from './components/input-forms'
import VideoStreamers from './components/video-streamers'

import { Snackbar } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import amber from '@material-ui/core/colors/amber';
import MarkersMap from './components/map'

const useStyles = makeStyles((theme) => ({
    success: {
      backgroundColor: green[600],
    },
    error: {
      backgroundColor: theme.palette.error.dark,
    },
    info: {
      backgroundColor: theme.palette.primary.main,
    },
    warning: {
      backgroundColor: amber[700],
    },
  }));


  const App = (props) => {
    const classes = useStyles();
    const [state, setState] = useState({
        urls: [],
        videoalignment: 'video',
        open: false,
        message: '',
        variant: 'success'
    });

    const isVideoAndStatistic = state.videoalignment === 'statistic';  
    const { open, message, variant } = state;
    const snackbarRef = useRef(null);

    const handleOpen = (message, variant) => {
        setState({ ...state, open: true, message, variant });
    };

    const handleClose = () => {
        setState({ ...state, open: false });
    };
   
    const  updateurls = (urls)=>{
     //convert from one format [[1,'url1'], [1,'url2']] to another [{cam:0, url:url}, {{cam:1, url:ur2}}] 
     //const urls_ = urls.map( data => { var l = {cam:data[0], url:data[1] }; return l; }); 
     setState({...state, urls});
  }

  const updateparams = (param) => {
      setState({...state, ...param}); 
  }

  const loadData = () => {  
    const DEFAULT_QUERY = global.config.API + "urls?list=true"
   
    //const deleteURL = URL + "?delete="
    setState({...state, isLoading: true });
   
    fetch(DEFAULT_QUERY)
        .then(response => {
            //console.log(" response:" + response)
            if (response.ok) {
                //console.log(" response:" + JSON.stringify(response, null, 2) )
                setState({...state, isLoading: false })
                return response.json();
            } else {
                console.log(" error:")
                throw new Error('Something went wrong ...');
            }
        })
        .then(data => {
             setState({ ...state, data, isLoading: false })
             updateurls(data);
             return data;
            })
        .catch(error => setState({...state, error, isLoading: false }));
    }
    useEffect(() => {
        console.log(props.req);
        loadData()
    }, []);

    return (  
        <div className="App"> 
          <SnackbarProvider value={{ handleOpen, handleClose }}>
          <header className="App-header">
                <MarkersMap markers={state.urls}/>      
                <div className="container">
                   <div className="row nav-wrapper"/> 
                   <div className="col-md-12">
                            <Snackbar 
                                open={open} 
                                message={message} 
                                variant={variant} 
                                onClose={handleClose} 
                                autoHideDuration={6000} 
                                ref={snackbarRef}
                                className={classes[variant]}/>
    
                            
                            <p> The smart cloud storage solution for video streams from public cameras. Our platform is powered by 5 ODROID ARM computers running 100% Python and 100% React, ensuring optimal performance and user experience.

At AIcams.info, we are dedicated to providing state-of-the-art deep learning algorithms to track and analyze video streams from surveillance cameras. Our platform enables you to test multiple deep learning networks on existing video streams and receive real-time insights and analysis.

With AIcams.info, you have the ability to enter the URL of any public IP camera and access its video stream from our platform. However, please note that by specifying the IP address or camera URL, you will be sharing your link with all other subscribers. To make your link private, you will need to subscribe to our payable version.

Enhance your surveillance capabilities with AIcams.info - try us today! <a href="http://aicams.info" class="arrow-btn">aicams.info</a> 
</p>

                            <h3> This is free smart cloud storage  for cameras video streams works on 5 ODROID ARM computers   (100% python, 100% React, for more information check 
                            <a href="//aicams.info" target="_blank" rel="noopener noreferrer"> http://aicams.info</a> ), bellow public available video-streams: </h3>
                           {/*The way to reference child component ref={(cd) => this.child = cd} */}
    
                            <InputURL updateparams={updateparams} /> 
    
                            {isVideoAndStatistic && <URLlist updateparams={updateparams} updateurls={updateurls} data={state.urls}/> }
                    </div>
                </div>
     
           </header>
        
            <VideoStreamers param={state} urls={state.urls} />
     
            <div className="feature-bg">
                <div className="row">
                    <div className="col-md-12 nopadding">
                        <div className="features-slider">
                            <ul className="slides" id="featuresSlider">
                                <li>
                                    <h1>Counting objects</h1>
                                    <p>
                                        Appling existing  <a href="https://www.pyimagesearch.com/2020/01/27/yolo-and-tiny-yolo-object-detection-on-the-raspberry-pi-and-movidius-ncs/">YOLO Tiny V3</a>
                                        Model network to surveillance cameras live video streams <a href="http://aicams.ca" className="arrow-btn">aicams.ca</a> to
                                        calculate occupancy number on video screen
                                    </p>
                                </li>
    
                                <li>
                                    <h1>Check Objects behaviour :</h1>
                                    <p>
                                    Check if object of interest behave accordingly. 
                        Check if object of interest was found  notify immediatly by eMail, SMS or voice call
                        You can buy full source code version of our cloud solution plus hardware (ARM computer) from our store : <a href="//aicams.info" target="_blank">http://aicams.info</a>.                                </p>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
    
        </SnackbarProvider>             
        </div>
      );}
    
export default App;

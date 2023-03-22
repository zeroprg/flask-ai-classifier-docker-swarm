import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios'
//import { groupBy } from 'lodash';

import { SnackbarProvider } from './snackbarContext';

import URLlist from './components/urls'
import InputURL from './components/input-forms'
import VideoStreamers from './components/video-streamers'

import { Snackbar } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import amber from '@material-ui/core/colors/amber';
import MarkersMap from './components/map'
import countries from './countries';

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
        videoalignment: 'video',
        open: false,
        message: '',
        variant: 'success'
    }); 

    const [initialUrls, setInitialUrls] = useState([]);
    const [descUrls, setDescUrls] = useState({});
    const [urls, setUrls] = useState([]);
    const [videoAlignment, setVideoAlignment] = useState('video');
    const [open, setOpen] = useState(false);
    const [isLoading, setLoading] = useState(false)
    const [message, setMessage] = useState('');
    const [variant, setVariant] = useState('success');

    const [countryFilter, setcountryFilter] = useState('RU');
    const [interestFilter, setinterestFilter] = useState('none');
    const isVideoAndStatistic = videoAlignment === 'statistic';  
    // State to hold grouped urls
    const [groupedUrls, setGroupedUrls] = useState({});
    const snackbarRef = useRef(null);

    const handleOpen = (message, variant) => {
        setMessage(message);
        setVariant(variant);
        setOpen(true);
    };

    const handlecountryFilterChange = (event) => {
        const selectedCountry = event.target.value;
        setcountryFilter(selectedCountry);
        setinterestFilter('none');
        setUrls(selectedCountry === 'all' ? initialUrls : initialUrls.filter((url) => url.country === selectedCountry));
    };
   
    const handleinterestFilterChange = (event) => {
      const selectedInterest = event.target.value;
      setinterestFilter(selectedInterest);
      setUrls(selectedInterest === 'all' ? initialUrls : initialUrls.filter((url) => url.objects_counted >= 0));
  };
    
    const handleClose = () => {
        setOpen(false);
    };
   
    const  updateurls = (initialUrls)=>{        
        setUrls( (countryFilter === 'all' ? initialUrls : initialUrls.filter((url) => url.country === countryFilter)) );
    }

  const updateparams = (param) => {
      setState({...state, ...param}); 
  }

  


  const loadData = () => {
    const DEFAULT_QUERY = global.config.API + 'urls?list=true';
  
    setLoading(true);
  
    axios
      .get(DEFAULT_QUERY)
      .then(response => {
        if (response.status === 200) {
          setLoading(false);
          return response.data;
        } else {
          console.log('error:');
          throw new Error('Something went wrong ...');
        }
      })
      .then(data => {
        setLoading(false);       
        setInitialUrls(data)
        updateurls(data);
        setGroupedUrls(groupUrlsByCountry(data));
        setDescUrls(groupUrlsByDesc(data));
      })
      .catch(error => setLoading(false));
    };
 
    // Function to group urls by country
    const groupUrlsByCountry = (urls) => {
        return urls.reduce((acc, cur) => {
        if (cur.country in acc) {
            acc[cur.country].push(cur);
        } else {
            acc[cur.country] = [cur];
        }
        return acc;
        }, {});
    };
        // Function to group urls by country
    const groupUrlsByDesc = (urls) => {
        return urls.reduce((acc, cur) => {
        if (cur.desc in acc) {
            acc[cur.desc].push(cur);
        } else {
            acc[cur.desc] = [cur];
        }
        return acc;
        }, {});
      };
    


    useEffect(() => {
        console.log(props.req);
        loadData()
    }, []);

    return (  
        <div className="App"> 
          <SnackbarProvider value={{ handleOpen, handleClose }}>
          <header className="App-header">
          {!isLoading && (
                <div>
                    <label htmlFor="interestFilter">Filter by:</label>
                    <select id="interestFilter" value={interestFilter} onChange={handleinterestFilterChange}>
                        <option key='interest' value='none'></option> 
                        <option key='rating' value='rating'>Rating</option>
                        {Object.keys(descUrls).sort().map((desc) => (
                          <option key={desc} value={desc}>
                            {desc}
                          </option>
                         ))}
                    </select>
                    <label htmlFor="countryFilter">Filter by country:</label>
                    <select id="countryFilter" value={countryFilter} onChange={handlecountryFilterChange}>                        
                        {Object.keys(groupedUrls).sort().map((countryCode) => (
                        <option key={countryCode} value={countryCode}>
                            {countries.find((c) => c.cc === countryCode) ? countries.find((c) => c.cc === countryCode).name : countryCode}
                        </option>
                        ))}                        
                    </select>                    
                </div>
          )}
                <MarkersMap key={countryFilter} markers={urls}/>      
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

At <a href="http://Bloberryconsulting.com">Bloberry Consulting </a>, we are dedicated to providing state-of-the-art deep learning algorithms to track and analyze video streams from surveillance cameras. Our platform enables you to test multiple deep learning networks on existing video streams and receive real-time insights and analysis.
Only filtered cameras are available now. This way none of the cameras on this site invade anybody's private life.
Any private or unethical camera will be removed immediately upon e-mail complaint. Please provide a direct link to help facilitate the prompt removal of the camera.
If you do not want to contact us by e-mail (zeroprg@yahoo.com), you can still remove your camera from site. The only thing you need to do is to set the password of your camera.
With AIcams.info, you have the ability to enter the URL of any public IP camera and access its video stream from our platform. However, please note that by specifying the IP address or camera URL, you will be sharing your link with all other subscribers. To make your link private, you will need to subscribe to our payable version.

Enhance your surveillance capabilities with AIcams.info - try us today! <a href="http://aicams.info" className="arrow-btn">aicams.info</a> 
</p>
    
                            <InputURL updateparams={updateparams} />    
                            {isVideoAndStatistic && <URLlist updateparams={updateparams} updateurls={updateurls} data={urls}/> }
                    </div>
                </div>
     
           </header>
        
            <VideoStreamers param={state} urls={urls} />
     
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

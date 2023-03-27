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

import t from './translator';



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
   
    const [urls, setUrls] = useState([]);
    const [videoAlignment] = useState('video');
    const [open, setOpen] = useState(false);
    const [isLoading, setLoading] = useState(false)
    const [message, setMessage] = useState('');
    const [variant, setVariant] = useState('success');

    const [countryFilter, setcountryFilter] = useState('RU');
    const [cityFilter, setcityFilter] = useState('none');
    const [interestFilter, setinterestFilter] = useState('none');
    const isVideoAndStatistic = videoAlignment === 'statistic';  
    // State to hold grouped urls
    const [groupedUrls, setGroupedUrls] = useState({});
    const [cityUrls, setCityUrls] = useState({});
    const [descUrls, setDescUrls] = useState({});
    
    const snackbarRef = useRef(null);

    const handleOpen = (message, variant) => {
        setMessage(message);
        setVariant(variant);
        setOpen(true);
    };
    const rated = initialUrls.filter((url) => url.objects_counted >= 0);

    const handlecountryFilterChange = (event) => {
        if( countryFilter ==='none' && interestFilter === 'none' ) return
        const selectedCountry = event.target.value;
        if( interestFilter === 'rating' ){          
          setUrls(countryFilter ==='none' ?  rated: groupedUrls[selectedCountry].filter((url) => url.objects_counted >= 0));        }
        else {  
          setUrls(selectedCountry === 'none' ? descUrls[interestFilter]:  (interestFilter === 'none'? groupedUrls[selectedCountry]:  groupedUrls[selectedCountry].filter(item=>item.desc===interestFilter)))        
        }
        setcityFilter('none')
        setcountryFilter(selectedCountry);
    };

    const handlecityFilterChange = (event) => {
      if( countryFilter ==='none' && cityFilter === 'none' ) return
      const selectedCity = event.target.value;      
      setUrls(selectedCity === 'none' ? groupedUrls[countryFilter]: cityUrls[selectedCity])        
      setcityFilter(selectedCity);
  };
   
    const handleinterestFilterChange = (event) => {
      if( countryFilter ==='none' && interestFilter === 'none' ) return
      const selectedInterest = event.target.value;    
      if( selectedInterest === 'rating' ){       
        setUrls(countryFilter ==='none' ?  rated: rated.filter(item=>item.country===countryFilter) );
      }
      else{
        setUrls( countryFilter ==='none' ? descUrls[selectedInterest] : (selectedInterest === 'none'? groupedUrls[countryFilter]:  groupedUrls[countryFilter].filter(item=>item.desc===selectedInterest)));
      }
      setcityFilter('none')
      setinterestFilter(selectedInterest);
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
        setCityUrls(groupUrlsByCity(data));
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

    // Function to group urls by city
    const groupUrlsByCity = (urls) => {
        return urls.reduce((acc, cur) => {
        //const city_code =  cur.city + ','+ cur.country;
        if (cur.city in acc) {
            acc[cur.city].push(cur);
        } else {
            acc[cur.city] = [cur];
        }
        return acc;
        }, {});
    };

        // Function to group urls by scene description
    const groupUrlsByDesc = (urls) => {
        return urls.reduce((acc, cur) => {
        if( cur.desc === null || cur.desc === 'null' ) return acc;        
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
                    <label htmlFor="interestFilter">{t("filter_class").__html}&nbsp;</label>&nbsp;
                    <select id="interestFilter" value={interestFilter} onChange={handleinterestFilterChange}>
                        <option key='none' value='none'></option> 
                        <option key='rating' value='rating'>Rated</option>
                        {Object.keys(descUrls).sort().map((desc) => (
                          <option key={desc} value={desc}>
                            {desc}
                          </option>
                         ))}
                    </select>
                    &nbsp;<label htmlFor="countryFilter">{t("filter_country").__html}&nbsp;</label>&nbsp;
                    <select id="countryFilter" value={countryFilter} onChange={handlecountryFilterChange}>                        
                        <option key='none' value='none'></option>
                        {Object.keys(groupedUrls).sort().map((countryCode) => (
                        <option key={countryCode} value={countryCode}>
                            {countries.find((c) => c.cc === countryCode) ? countries.find((c) => c.cc === countryCode).name : countryCode}
                        </option>
                        ))}                        
                    </select>
                    &nbsp;<label htmlFor="cityFilter">{t("filter_city").__html}&nbsp;</label>&nbsp;
                    <select key={handlecountryFilterChange} id="cityFilter" value={cityFilter} onChange={handlecityFilterChange}>                        
                        <option key='none' value='none'></option>                       
                         {groupedUrls[countryFilter] && groupedUrls[countryFilter].map((url) => (
                          <option key={url.id} value={url.city}>
                            {url.city}
                          </option>                          
                         ))}       
                                                                
                    </select>                     
                </div>
          )}
                <MarkersMap markers={urls}/>      
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
                            
                            <p dangerouslySetInnerHTML={t("site_desc")}/> 
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

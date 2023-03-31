import React, { useState, useRef, useEffect } from 'react';
import { Picker, StyleSheet, View, Text, ScrollView  } from 'react-native';

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
    const [interestFilter, setinterestFilter] = useState('person');
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
        Promise.resolve().then(() => {
          return loadData();
        });
    });
    return (
    <View style={styles.container}> 
    <SnackbarProvider value={{ handleOpen, handleClose }}>
      <View style={styles.filterContainer}>
      {!isLoading && (
        <View style={styles.filterContent}>
          <Text>{t("filter_class").__html}&nbsp;</Text>
          <Picker
            style={styles.picker}
            selectedValue={interestFilter}
            onValueChange={handleinterestFilterChange}
          >
            <Picker.Item key='none' value='none' label='' />
            <Picker.Item key='rating' value='rating' label='Rated' />
            {Object.keys(descUrls)
              .sort()
              .map((desc) => (
                <Picker.Item key={desc} value={desc} label={desc} />
              ))}
          </Picker>
          <Text>{t("filter_country").__html}&nbsp;</Text>
          <Picker
            style={styles.picker}
            selectedValue={countryFilter}
            onValueChange={handlecountryFilterChange}
          >
            <Picker.Item key='none' value='none' label='' />
            {Object.keys(groupedUrls)
              .sort()
              .map((countryCode) => (
                <Picker.Item
                  key={countryCode}
                  value={countryCode}
                  label={
                    countries.find((c) => c.cc === countryCode)
                      ? countries.find((c) => c.cc === countryCode).name
                      : countryCode
                  }
                />
              ))}
          </Picker>
          <Text>{t("filter_city").__html}&nbsp;</Text>
          <Picker
            key={handlecountryFilterChange}
            style={styles.picker}
            selectedValue={cityFilter}
            onValueChange={handlecityFilterChange}
          >
            <Picker.Item key='none' value='none' label='' />
            {groupedUrls[countryFilter] &&
              groupedUrls[countryFilter].map((url) => (
                <Picker.Item key={url.id} value={url.city} label={url.city} />
              ))}
          </Picker>
        </View>
      )}
      </View>
      <View style={{ flex: 1 }}>
        <MarkersMap markers={urls}/>
        <View style={{ flex: 1 }}>
          <Snackbar 
            visible={open} 
            onDismiss={handleClose} 
            duration={6000}
            style={variant === "error" ? {backgroundColor: "red"} : {backgroundColor: "green"}}
          >
            {message}
          </Snackbar>
          <Text>{t("site_desc")}</Text>
          <InputURL updateparams={updateparams} />    
          {isVideoAndStatistic && <URLlist updateparams={updateparams} updateurls={updateurls} data={urls}/> }
        </View>
      </View>

      <VideoStreamers param={state} urls={urls} />

      <View style={styles.featureBg}>
        <ScrollView horizontal={true}>
          <View style={styles.featureSlide}>
            <Text style={styles.featureHeader}>{t("bottom_word1_header").__html}</Text>
            <Text style={styles.featureText}>{t("bottom_word1").__html}</Text>
          </View>
          <View style={styles.featureSlide}>
            <Text style={styles.featureHeader}>{t("bottom_word2_header").__html}</Text>
            <Text style={styles.featureText}>{t("bottom_word2").__html}</Text>
          </View>
        </ScrollView>
      </View>
      </SnackbarProvider>
   </View>);}

    
export default App;

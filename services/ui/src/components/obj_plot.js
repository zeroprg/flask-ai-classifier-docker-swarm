import React, { useEffect, useState } from 'react'
import TimeRange from './time_range'
import { makeStyles } from '@material-ui/core/styles';
//import {XYPlot, XAxis, YAxis, HorizontalGridLines, VerticalGridLines, VerticalBarSeries} from 'react-vis';
import SelectObj from './obj_select';
import Plotter from './plotter';


 const ObjectOfInterestPlot = (props) => {

      const DEFAULT_QUERY =  global.config.API + "moreparams?cam=" + props.cam +"&hour_back1=" +
            props.timerange.start + "&hour_back2="  + props.timerange.end + "&object_of_interest="
      const BASIC_COLOR = parseInt('0x008B8B', 16) //#12939A'
   
      const [timerange, setTimerange] = useState(props.timerange);
      const [data, setData]  = useState({})
      const [color, setColor] = useState(BASIC_COLOR)
      const [selected_obj_of_interest, setObjectOfInterest]  = useState([props.object_of_interest[0]])
      const [time, setTime] = useState( new Date().getTime());
   
      const useStyles = makeStyles({
        root: {
          paddingLeft: '20px',
        },
      });
      const classes = useStyles();
 
    async function fetchStatisticData(objectOfInterest) {
      
      fetch(DEFAULT_QUERY + objectOfInterest)
          .then(response => {
              // make sure to check for errors
              console.log(" response:" + response)
              if (response.ok) {
                  console.log(" response:" + JSON.stringify(response, null, 2) )
                  return response.json();
              } else {
                  console.log(" error:")
                  throw new Error('Something went wrong ...');
              }              
          })
          .then(val => { 
              if( val && val.length>0) {
                setColor(color + 100)       
                setData(val); 
              }
              return val;              
          })
     }
    function fetchAll(){
      if(selected_obj_of_interest) 
          fetchStatisticData(selected_obj_of_interest);
    }



    useEffect(() => {
      const interval = setInterval(() => setTime(new Date().getTime()), 600000);
      return () => {
        clearInterval(interval);
      };
    }, []);

    useEffect(() => { 
      setColor(BASIC_COLOR)   
      fetchAll();
      },[props.cam, selected_obj_of_interest, timerange, time]);


      

    function onTimeChanged(timerange){
      setTimerange(timerange);
      props.onTimeChanged(timerange);
    }

    
    function onParamsChanged(object_of_interest ){
      setObjectOfInterest(object_of_interest);
      props.onParamsChanged(object_of_interest);
    }
    return (
    <div className={classes.root}>
      <TimeRange onParamsChanged={onTimeChanged} timerange={props.timerange}/>
      <SelectObj onParamsChanged={onParamsChanged} 
                 object_of_interest={props.object_of_interest}
                 selected_object_of_interest={[props.object_of_interest[0]]}/>
      <Plotter id="plotter" key={timerange} data={data} timerange = {timerange} /> 
    </div>
    );
  }
  
export default ObjectOfInterestPlot
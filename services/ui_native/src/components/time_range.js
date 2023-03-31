import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';

const useStyles = makeStyles({
  root: {
    width: 600,
  },
});

function valuetext(value) {
  return value + ' hours';
}

const RangeSlider = (props) => {
  const classes = useStyles();
  const [value, setValue] = React.useState([props.timerange.start, props.timerange.end]);

  const handleChange = (event, newValue) => {
    const timerange = {start: newValue[0], end: newValue[1]} 
    props.onParamsChanged(timerange);
    setValue(newValue);
  };

  return (
    <div className={classes.root}>
      <Typography id="range-slider" gutterBottom>
        Time range (between {value[0]} and {value[1]} hours back)
      </Typography>
      <Slider
        value={value}
        onChange={handleChange}
        valueLabelDisplay="auto"
        aria-labelledby="range-slider"
        getAriaValueText={valuetext}
      />
    </div>
  );
}
export default RangeSlider
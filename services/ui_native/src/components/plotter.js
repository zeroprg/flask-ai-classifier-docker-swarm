import React, { useState, useEffect } from 'react';
import { XYPlot, XAxis, YAxis, VerticalGridLines,  HorizontalGridLines,  VerticalBarSeries} from 'react-vis';
const Plotter = (props) => {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => {
      setWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const time = Math.floor(new Date().getTime());
  const ONE_HOUR = 3600000;
  
  const handleBarClick = (value) => {
    props.onBarClick(value);
}

   return (props && props.data.length > 0) ?(
      <XYPlot xType="time" style={{ align: 'center' }} width={width} height={230}
        xDomain={[time - props.timerange.end * ONE_HOUR, time - props.timerange.start * ONE_HOUR]}>
        <HorizontalGridLines />
        <VerticalGridLines />
        <XAxis title="time" />
        <YAxis title="Frequency" />
        {props.data.map(data =>
          <VerticalBarSeries key={data.label} data={data.values}   onValueClick={value => handleBarClick(value)} />
        )}
      </XYPlot>
    ):""
  
};

export default Plotter;

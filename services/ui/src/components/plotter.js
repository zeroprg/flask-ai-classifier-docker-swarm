import React, { Component } from 'react';
import { XYPlot, XAxis, YAxis, VerticalGridLines,  HorizontalGridLines,  VerticalBarSeries} from 'react-vis';

class Plotter extends Component {

    componentDidMount() {        
        window.addEventListener("resize", this.resize.bind(this));
        this.resize();
    }
    
    resize() {
        this.setState({width: window.innerWidth*0.6 });
    }    


    componentWillUnmount() {
        window.removeEventListener("resize", this.resize.bind(this));
    }


    render() {
        const time =  Math.floor(new Date().getTime()); // in mil. sec.
       // const labels = this.props.data.map(data => data.label); // [...new Set()]
        //const ONE_DAY = 3600000*24;
        //{Object.entries(this.props.data).map(([key, value]) =>
        //  xDomain={[ time - this.props.timerange.end*ONE_HOUR, time - this.props.timerange.start*ONE_HOUR ]}

        const ONE_HOUR = 3600000;
        if( this.props && this.props.data.length>0)
        
        return (
            
            <XYPlot xType="time" width={this.state.width}  height={230}
                xDomain={[ time - this.props.timerange.end*ONE_HOUR, time - this.props.timerange.start*ONE_HOUR ]}
            >


            <HorizontalGridLines />
            <VerticalGridLines />
            <XAxis title="time" />
            <YAxis title="Frequency" />
            
            { this.props.data.map( data =>
                <VerticalBarSeries key = {data.label}  data = {data.values} />
            )}
            </XYPlot>
        
            );
         else 
            return (
                <img src={'img/fancybox_loading.gif'}></img>
              );
        
        }  
}
export default Plotter;
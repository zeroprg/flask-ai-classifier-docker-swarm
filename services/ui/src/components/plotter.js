import { map } from 'd3';
import React, { Component } from 'react';
import { XYPlot, XAxis, YAxis, VerticalGridLines,  HorizontalGridLines,  VerticalBarSeries, DiscreteColorLegend, VerticalRectSeries} from 'react-vis';

class Plotter extends Component {
    componentDidMount() {
        window.addEventListener("resize", this.resize.bind(this));
        this.resize();
    }
    
    resize() {
        this.setState({width: window.innerWidth });
    }
    
    componentWillUnmount() {
        window.removeEventListener("resize", this.resize.bind(this));
    }


    render() {
        const time =  Math.floor(new Date().getTime());; // in mil. sec.
        //const ONE_DAY = 3600000*24;
        //{Object.entries(this.props.data).map(([key, value]) =>
        //  xDomain={[ time - this.props.timerange.end*ONE_HOUR, time - this.props.timerange.start*ONE_HOUR ]}

        const ONE_HOUR = 3600000;
        if( this.props && this.props.data.length>0)
        return (

            <XYPlot xType="time" width={this.state.width}  height={300}
                xDomain={[ time - this.props.timerange.end*ONE_HOUR, time - this.props.timerange.start*ONE_HOUR ]}
            >
                <DiscreteColorLegend
                    style={{position: 'absolute', left: '10px', top: '10px'}}
                    orientation="horizontal"
                    items=  {this.props.data.map(data => data.label)}
                />

            <HorizontalGridLines />
            <VerticalGridLines />
            <XAxis title="time" />
            <YAxis title="Frequency" />
            
            { this.props.data.map( data =>
                <VerticalRectSeries key = {data.label}  data = {data.values} />
            )}
            </XYPlot>
        
            );
         else 
            return (
                <div className="loading"> ... Loading </div>
              );
        
        }  
}
export default Plotter;
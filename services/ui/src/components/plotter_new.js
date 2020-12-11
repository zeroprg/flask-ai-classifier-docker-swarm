import React, { Component } from "react";
import { LineChart, ScatterPlot, Brush } from "react-d3-components";
import * as d3 from 'd3';
class Plotter extends Component {
    ONE_DAY = 3600000*24;
     tooltipScatter = (x, y) => {
        return "x: " + x  + " y: " + y;
    };

    recalculateParameters(){
        const timestamp = Math.floor(new Date().getTime());
        const ONE_HOUR = 3600000;
        const start = timestamp - this.props.timerange.end*ONE_HOUR
        const end   = timestamp - this.props.timerange.start*ONE_HOUR
        this.extent = [ start , end ]

        this.setState({data: this.props.data,
            xScale: d3.scaleTime().domain([start, end]).range([0, 1000 - 70]),
            xScaleBrush: d3.scaleTime().domain([start, end]).range([0, 1000 - 70])
            });    
    } 

    componentDidMount(){
        this.setState({timerange: this.props.timerange})
        this.recalculateParameters();    
    }

    componentWillReceiveProps(nextProps) {
        // You don't have to do this check first, but it can help prevent an unneeded render
        if( Object.keys(this.props.data).length > 0 && this.props.data.values.length>0 &&
          (nextProps.timerange.start !== this.state.timerange.start || nextProps.timerange.end !== this.state.timerange.end)) {
          this.setState({timerange: nextProps.timerange})    
          this.recalculateParameters();    
        }
      }

    _onChange = (extent) => {
        this.setState({xScale: d3.scaleTime().domain([extent[0], extent[1]]).range([0, 1000 - 70])});
    }


    render(){
//        xAxis={{tickValues: this.state.xScale.ticks(d3.timeDays, 2), tickFormat: d3.timeFormat("%m/%d")}}
    if( this.state && Object.keys(this.state.data).length > 0 && this.props.data.values.length>0){
        
        return (
        <div>
            <ScatterPlot
                    data={this.state.data}
                    width={1000}
                    height={300}
                    margin={{top: 10, bottom: 50, left: 50, right: 10}}
                    tooltipHtml={this.tooltipScatter}
                    yAxis={{label: "Quantity"}}
                    xScale={this.state.xScale}
                    xAxis={()=>this.state.xScale.ticks(d3.timeDays, 2).tickFormat(d3.timeFormat("%m/%d"))}
     
                />,

            <div className="brush" width={1000} style={{float: 'none'}}>
                <Brush
                width={1000}
                height={50}
                margin={{top: 0, bottom: 30, left: 50, right: 20}}
                xScale={this.state.xScaleBrush}
                extent={this.extent}
                xAxis={()=>this.state.xScale.ticks(d3.timeDays, 2).tickFormat(d3.timeFormat("%m/%d"))}
                onChange={this._onChange}

                />
            </div>
        </div>
    ); }
    else 
    return (
        <div className="loading"> ... Loading </div>
      );

 } 
}

export default Plotter
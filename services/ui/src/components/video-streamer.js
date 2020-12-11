import React, { Component } from 'react';
import { Tabs, Tab } from 'react-bootstrap';
import SelectObj from './obj_select';

import ObjectOfInterestPlot from './obj_plot'
import ObjectOfInterest from './objects_of_interest'
import Video from './video';

class VideoStreamer extends Component {
    
    

    componentWillMount() {
        // initial state
    this.setState({
        isLoading : false,
        timerange: {start: 0, end: 1},
        object_of_interest: this.props.object_of_interest
        })
    }

    onTimeChanged = (timerange)=>{
            this.setState( {timerange: timerange} );
    }

    onParamsChanged = (object_of_interest)=>{
            this.setState( {object_of_interest: object_of_interest});
    }

    render() {
        //const { error } = this.state;
        const { camera } = this.props;
/*
        if (error) {
            return <p>{error.message}</p>;
        }
*/
        
        return (            
                <section id={'section'+camera.cam} key={'section'+camera.cam} style={{display: 'block'}}>
                    <div className="row">
                        <div className="col-sm-12">
                          <ObjectOfInterestPlot cam={camera.cam}
                                                timerange={this.state.timerange} 
                                                onParamsChanged={this.onParamsChanged.bind(this)}
                                                onTimeChanged={this.onTimeChanged.bind(this)}
                                                object_of_interest={this.props.object_of_interest}/>
                        </div> 
                    </div> {/* className row */}

                <div className="row">
                <div className="col-sm-6">
                    <Video key={camera.cam} camera = {camera} showBoxes={false}/> 
                </div>  
                <div className="col-sm-6">                           
                    <Tabs  defaultActiveKey="founded_objects" id="uncontrolled-tab">
                        <Tab eventKey="founded_objects" title="Founded Objects" className="tabcontent">
                            <ObjectOfInterest object_of_interest={this.state.object_of_interest}
                                timerange={this.state.timerange}
                                cam={camera.cam}
                            />    
                        </Tab>
    {/*                 <Tab eventKey="events" title="Events Notify" className="tabcontent">
                        <h3>Events notifyer</h3>
                            <p>Specify Events which will triger eMail or SMS/Voice notify.</p>
                            <select name="objects">
                                <option value="person">person</option>
                                <option value="car">car</option>
                                <option value="dog">dog</option>
                                <option value="cat">cat</option>
                            </select> and 
                            <select name="quantity">
                                <option value="quantity">quantity</option>
                                <option value="time">time(sec.)</option>
                            </select> 
                            <select name="&gt;>">
                                <option value={'&gt;'}>&gt;</option>
                                <option value={'&lt;'}>&lt;</option>
                                <option value="=">=</option>
                            </select>              
                            <input type="number" id="quantity" name="quantity" placeholder="0" min="0" max="100" />
                            <br/>
                            Notify me by 
                            <select name="eMail;>">
                                <option value="email;">email</option>
                                <option value="sms">SMS</option>
                                <option value="voice">voice</option>
                            </select> 
                            :
                            <input type="text" placeholder="" min="0"  max="100" />
                        </Tab> 
                */}       
                    </Tabs>
                    </div>  {/*<div className="col-sm-6">*/}
                </div> {/* className row */}
            </section>                       
            );
        }
}
export default VideoStreamer
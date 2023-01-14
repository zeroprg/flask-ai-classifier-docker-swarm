import React, { Component } from 'react';
import { FormControl,RadioGroup,FormControlLabel, Radio } from '@material-ui/core';

class InputURL extends Component {
    state = {isLoading: false , videoalignment: 'video'};
    constructor(props) {
        super();
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
      }
    
      updateparams(param) {
        this.props.updateparams(param);
      }
    
      handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox'  ? target.checked : target.value;
        const name = target.name;
        
        this.setState({ [name]: value });
        this.updateparams({ [name]: value });
        
      }

      handleSubmit(event) {
        this.props.addURL(this.state.url)         
        event.preventDefault();
      }
    
     
    render() {
        return (
            <div>
                {this.state.isLoading? <img src={'img/fancybox_loading.gif'}></img>:''} 
                <h3>Enter IP Camera url at this box </h3>
                <h3><b>Warning:</b> "By specifying IP Address or camera URL bellow you will share your link with all other subscribers. To make this link private your have to subscribe to payable version"</h3>
                    <form id="myform" className="form-horizontal" onSubmit={this.handleSubmit}>
                            <div className="form-group">
                                <label className="control-label col-sm-2" htmlFor="pwd">URL:</label>
                                <div className="col-sm-12">
                                    <input type="URL" className="form-control" id="url" name="url" placeholder="Enter Camera ip or URL address here (analyse will started after 100 secs, be pation)"
                                           value={this.state.url} onChange={this.handleInputChange}/>
                                </div>
                            </div>
                  {/*          <div className="form-group">
                                <label className="control-label col-sm-2" htmlFor="email">Email:</label>
                                <div className="col-sm-10">
                                    <input type="email" className="form-control" id="email" placeholder="someone@example.com" name="email"
                                            value={this.state.email} onChange={this.handleInputChange}/>
                                </div>
                              </div>  
             */}             
                            
                            <div className="form-group">
                                <div className="col-sm-offset-2 col-sm-12">
                                    <input type="submit" value="Submit" className="btn btn-primary a-btn - slide - text"/>                                    
                                </div>
                            </div>
                            <FormControl component="fieldset">
                                <RadioGroup row aria-label="videoalignment" name="videoalignment" value={this.state.videoalignment} onChange={this.handleInputChange}>
                                    <FormControlLabel value="video" control={<Radio />} label="Show only video" />
                                    <FormControlLabel value="statistic" control={<Radio />} label="Show video and cameras statisic" />
                                    <FormControlLabel value="both" control={<Radio />} label="Show captured objects and video" />
                                    <FormControlLabel disabled value="objects" control={<Radio />} label="Show captured objects only" />
                                </RadioGroup>
                           </FormControl>
                           
                    </form>
                </div>
                    )
        };
}

export default InputURL
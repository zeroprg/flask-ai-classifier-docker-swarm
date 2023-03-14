import React, { Component } from 'react';
import { FormControl,RadioGroup,FormControlLabel, Radio } from '@material-ui/core';
import axios from 'axios'
import { SnackbarConsumer } from '../snackbarContext';


class InputURL extends Component {
    state = {isLoading: false , videoalignment: 'video', url:""};
    
    constructor(props) {
        super();
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleClick = this.handleClick.bind(this);
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

 
      handleClick(handleOpen) {
        const URL = global.config.API + "urls"
        const payload = {
            add: this.state.url,
        }
        axios.post(URL, payload)
            .then(function (response) {
                console.log(response);
                handleOpen(response.data.message, 'success')
            })
            .catch(function (error) {
                console.log(error);
                handleOpen(error.response.data.message, 'error')
            });
      }

    

      

     
    render() {
        return (
            <SnackbarConsumer>
            {({ handleOpen}) => (    
            <div>
                {this.state.isLoading? <img src={'img/fancybox_loading.gif'}></img>:''} 
                <h3>Enter IP Camera url at this box </h3>
                <h3 style={{color: '#07ff7f'}}><b>Warning:</b> "By specifying IP Address or camera URL bellow you will share your link with all other subscribers. To make this link private your have to subscribe to payable version"</h3>
                <div className="form-group">
                    <label className="control-label col-sm-2" htmlFor="pwd">URL:</label>
                    <div className="col-sm-12">

                        <input type="URL" className="form-control" id="url" name="url" placeholder="Enter Camera ip or URL address here (analyse will started after 100 secs, be pation)"
                                value={this.state.url} onChange={this.handleInputChange}/>

                    </div>
                </div>
                            
                <div className="form-group">
                    <div className="col-sm-offset-2 col-sm-12">
                        <input type="button" value="Submit" className="btn btn-primary a-btn - slide - text" onClick={()=>this.handleClick(handleOpen)}/>                                    
                    </div>
                </div>

                {/*<form id="myform" className="form-horizontal">                        
                        <FormControl component="fieldset">
                            <RadioGroup row aria-label="videoalignment" name="videoalignment" value={this.state.videoalignment} onChange={this.handleInputChange}>
                                <FormControlLabel value="video" control={<Radio />} label="Show only video" />
                                <FormControlLabel value="statistic" control={<Radio />} label="Show captured objects only" />
                            </RadioGroup>
                        </FormControl>                           
                </form>
            */}
                
            </div>
            )}</SnackbarConsumer> )
        };
}

export default InputURL
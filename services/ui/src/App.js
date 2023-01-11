import React, { Component } from 'react';
import { alertService } from './components/alert/alert_services'; 
import { Alert } from './components/alert/alert';

import URLlist from './components/urls'
import InputURL from './components/input-forms'
import VideoStreamers from './components/video-streamers'




class App extends Component {
    state = { urls: [], videoalignment: 'video' }
    constructor(props) {
        super(props);

        this.state = {
            urls:[],
            videoalignment: 'video',
         //   autoClose: true,
         //   keepAfterRouteChange: false
        };
    }    

  saveURLForm(url) {
    const autoClose = true;
    const keepAfterRouteChange = true;            
    this.setState({ isLoading: true});
    const DEFAULT_QUERY = global.config.API + "urls?add="+ url + "&email="+this.state.email
    console.log(" start:")
    fetch(DEFAULT_QUERY)
        .then((response) => {
                this.setState({ isLoading: false, url: '' });
                const statusCode = response.status;
                switch(statusCode){
                case 500 : 
                    alertService.error('Error adding  <b>'+url+'</b> its already exist', { autoClose, keepAfterRouteChange })  
                    break;
                case 400 : 
                    alertService.error('Error adding  <b>'+url+'</b> no video on this url', { autoClose, keepAfterRouteChange })  
                    break;    
                case 200: {
                    this.state.urls.unshift(url);
                    this.setState({url:''});
                    alertService.success('Success!! ${url}', { autoClose, keepAfterRouteChange })
                 }
                }
              })
        .catch(error => {
            this.setState({ isLoading: false})
            alertService.error('Error for ${url}: ${error}', { autoClose, keepAfterRouteChange })
            });
    } 


  addNewURL(url){
  
    if(this.state.urls){
        for (const val of this.state.urls)
            if(val.url === url) {
                return
            }
        this.saveURLForm(url);
  //      this.setState({url:true})
//      setTimeout(this.setState, 1000,{url:true});
    }    
  }

  updateurls(urls){
     //convert from one format [[1,'url1'], [1,'url2']] to another [{cam:0, url:url}, {{cam:1, url:ur2}}] 
     //const urls_ = urls.map( data => { var l = {cam:data[0], url:data[1] }; return l; }); 
     this.setState({urls:urls});
  }

  updateparams = (param) => {
      this.setState(param); 
  }

  loadData() {  
    const DEFAULT_QUERY = global.config.API + "urls?list=true"
    const URL = global.config.API + "urls"
    const deleteURL = URL + "?delete="
    this.setState({ isLoading: true });
   
    fetch(DEFAULT_QUERY)
        .then(response => {
            console.log(" response:" + response)
            if (response.ok) {
                //console.log(" response:" + JSON.stringify(response, null, 2) )
                this.setState({isLoading: false })
                return response.json();
            } else {
                console.log(" error:")
                throw new Error('Something went wrong ...');
            }
        })
        .then(data => {
             this.setState({ data: data, isLoading: false })
             this.updateurls(data);
             return data;
            })
        .catch(error => this.setState({ error, isLoading: false }));
    }

    componentDidMount() {
        // initial state
        this.loadData()
    }  

  render() {
    const isVideoAndStatistic = this.state.videoalignment === 'statistic';  
    return (  
    <div className="App"> 

      <header className="App-header">
        <section className="hero">
            <div className="texture-overlay"></div>
            <div className="container">
               {/* <div className="row nav-wrapper"/> */}
               <Alert></Alert>
                <div className="hero-content">
                    <div className="col-md-12">
                        {/*<a href=""></a> */}
                    </div>
                    <div className="col-md-12">
                       
                        <h1 className="animated fadeInDown">AI processed video streams from public cameras.</h1>

                        <h3> This is free smart cloud storage  for cameras video streams works on ODROID ARM based computers   (100% python , no php  for more information check 
                        <a href="//aicams.info" target="_blank" rel="noopener noreferrer"> http://aicams.info</a> ), bellow public available video-streams: </h3>
                       {/*The way to reference child component ref={(cd) => this.child = cd} */}

                        <InputURL updateparams={this.updateparams.bind(this)}
                                  addURL={this.addNewURL.bind(this)}/> 
                               
                        {isVideoAndStatistic && <URLlist updateparams={this.updateparams.bind(this)} 
                                                         updateurls={this.updateurls.bind(this)}
                                                         data={this.state.urls}/> }
                         
                     </div>
                </div>
            </div>
        </section>
    </header>
    

       <VideoStreamers param={this.state} urls={this.state.urls} />

    
 
        <div className="feature-bg">
            <div className="row">
                <div className="col-md-12 nopadding">
                    <div className="features-slider">
                        <ul className="slides" id="featuresSlider">
                            <li>
                                <h1>Counting objects</h1>
                                <p>
                                    Appling existing  <a href="https://www.pyimagesearch.com/2020/01/27/yolo-and-tiny-yolo-object-detection-on-the-raspberry-pi-and-movidius-ncs/">YOLO Tiny V3</a>
                                    Model network to surveillance cameras live video streams <a href="http://aicams.ca" className="arrow-btn">aicams.ca</a> to
                                    calculate occupancy number on video screen
                                </p>
                            </li>

                            <li>
                                <h1>Check Objects behaviour :</h1>
                                <p>
                                Check if object of interest behave accordingly. 
                    Check if object of interest was found  notify immediatly by eMail, SMS or voice call
                    You can buy full source code version of our cloud solution plus hardware (ARM computer) from our store : <a href="//aicams.info" target="_blank">http://aicams.info</a>.                                </p>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

                    
    </div>
  );}
}
export default App;

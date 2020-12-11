import React, { Component } from 'react';
import { ToastContainer, toast } from 'react-toastify';
  import 'react-toastify/dist/ReactToastify.css';
  


import URLlist from './components/urls'
import InputURL from './components/input-forms'
import VideoStreamers from './components/video-streamers'

const notify = () => toast("This URL already exist !");



class App extends Component {
  state = { urls: [], videoalignment: 'video' }

  addNewURL(url){
  
    if(this.state.urls){
        for (const val of this.state.urls)
            if(val.url === url) {
                return
            }
        this.child.saveURLForm();
        this.setState({url:true})
        setTimeout(this.setState, 1000,{url:true});
    }    
  }

  updateurls(urls){
     //convert from one format [[1,'url1'], [1,'url2']] to another [{cam:0, url:url}, {{cam:1, url:ur2}}] 
     const urls_ = urls.map( data => { var l = {cam:data[0], url:data[1] }; return l; }); 
     this.setState({urls:urls_});
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
               {/* <div class="row nav-wrapper"/> */}

                <div className="hero-content">
                    <div className="col-md-12">
                        {/*<a href=""></a> */}
                    </div>
                    <div className="col-md-12">
                        <h1 className="animated fadeInDown">AI processed video streams from public cameras.</h1>
                        <h3> This is free smart cloud storage  for cameras video streams works on ODROID ARM based computers   (100% python , no php  for more information check 
                        <a href="//aicameras.ca" target="_blank" rel="noopener noreferrer"> http://aicameras.ca</a> ), bellow public available video-streams: </h3>
                        <InputURL updateparams={this.updateparams.bind(this)}
                                  ref={(cd) => this.child = cd}
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

    
 
        <div class="feature-bg">
            <div class="row">
                <div class="col-md-12 nopadding">
                    <div class="features-slider">
                        <ul class="slides" id="featuresSlider">
                            <li>
                                <h1>Counting objects</h1>
                                <p>
                                    Appling existing  <a href="https://www.pyimagesearch.com/2020/01/27/yolo-and-tiny-yolo-object-detection-on-the-raspberry-pi-and-movidius-ncs/">YOLO Tiny V3</a>
                                    Model network to surveillance cameras live video streams <a href="http://aicams.ca" class="arrow-btn">aicams.ca</a> to
                                    calculate occupancy number on video screen
                                </p>
                            </li>
                            <li>
                                <h1>Store Objects of interest:</h1>
                                <p>
                                    Any object of interest can be saved
                                    Trial version has only 1Gb storage to store statistic data, images and video
                                </p>
                            </li>
                            <li>
                                <h1>Check Objects behaviour :</h1>
                                <p>
                                Check if object of interest behave accordingly. 
                    Check if object of interest was found  notify immediatly by eMail, SMS or voice call
                    You can buy full source code version of our cloud solution plus hardware (ARM computer) from our store : <a href="//aicameras.ca" target="_blank">http://aicameras.ca</a>.                                </p>
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

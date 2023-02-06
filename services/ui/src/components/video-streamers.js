import React, { Component} from 'react';


import VideoStreamer from './video-streamer';
import VideoStat from './video-statist';

const object_of_interest = ['car','person'];
const timerange = {start: 0, end: 6};
class VideoStreamers extends Component {
    // shared between childs functions
    
    updateparams = (param) => {
        this.setState({param:param});
    }

 
    constructor(props) {
        super(props);
        this.state = {value: '' , showvideo: true};           
        this.url = props.url;
      }

      componentDidMount() {
        // initial state
        this.loadURLs()
    }    

    loadURLs() {
        const DEFAULT_QUERY =  global.config.API + "urls?list=true";
        this.setState({ isLoading: true });

        fetch( DEFAULT_QUERY )
            .then(response => {
                //console.log(" response:" + response)
                if (response.ok) {
                    //console.log(" response:" + JSON.stringify(response, null, 2) )
                    return response.json();
                } else {
                    console.log(" error:")
                    throw new Error('Something went wrong ...');
                }
            })
            .then(data => this.setState({ urls: data.urls, object_of_interest: object_of_interest, isLoading: false }))
            .catch(error => this.setState({ error, isLoading: false }));
    }

render() {
    const { urls } = this.props;
    const {  isLoading, error } = this.state;
    const { param } = this.props;
    const isOnlyVideos = param.videoalignment === 'video';
    const isStatistic = param.videoalignment === 'statistic';
    const isVideoAndStatistic = param.videoalignment === 'both';
    


    if (error) {
        return <p>{error.message}</p>;
    }

    if (isLoading) {
        return <p>Loading ...</p>;  
    }
    if (isOnlyVideos || isStatistic){
    return (
        <div className="row">
            {urls.map( camera => <VideoStat key={camera.url} camera={camera} timerange = {timerange}  object_of_interest={object_of_interest}/> )}
        </div>
        )
    } else if(isVideoAndStatistic) {    
    return (            
        <span>
            {urls.map( camera =>               
            <VideoStreamer key={camera.id} camera={camera} timerange = {timerange}  object_of_interest={object_of_interest}/>
        )}
        </span>
    );
    }
  }
}
export default VideoStreamers     

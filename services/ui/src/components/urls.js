import React, { Component } from 'react';

class URLlist extends Component {

buttonClickHide(arg1, arg2) {
    let elem = document.getElementById("section"+arg2)
    if(elem) elem.style.display ='none';
}
 constructor(){
     super();
     this.state = {data : []};
 }

 updateparams(param) {
    this.props.updateparams(param);
  }

 updateurls( data ) {
    this.setState( data )    
    this.props.updateurls(data);
 }

buttonClickShow(cam) {
    this.updateparams({ videoalignment: 'both' });
    let elem = document.getElementById("section"+cam);
    
    if (elem ) {
        elem.scrollIntoView();
    }    

}


/*
componentWillMount() {
        // initial state
    this.setState({
        data : [[0, "http://213.226.254.135:91/mjpg/video.mjpg"]],
        isLoading : false,
       // error: {message: 'URL is empty' }
    })
}    


                    <a  onClick={() =>  this.buttonClickHide(this.state.url+data[1] , data[0])} className="btn btn-primary a-btn - slide - text">
                        <span className="glyphicon" aria-hidden="true"></span>
                        <span>
                            <strong>Hide</strong>
                        </span>
                    </a>

*/
  


render() {
    const { data } = this.props;

    if(data && data.length>0)    
    return (
        <ul>
            {data.map(data =>
                <li key={data.cam}>
                    <a href={data.url}>{data.url}</a>
                    &nbsp;
                    <a onClick={() => this.buttonClickShow( data.url )} className="btn btn-primary a-btn - slide - text">
                        <span className="glyphicon" aria-hidden="true"></span>
                        <span>
                            <strong>Show</strong>
                        </span>
                    </a>
                </li>
            )}
        </ul>
    );
    else {
        return <p className= "loading"> ...  Loading ...</p>
    }
  }
}
export default URLlist
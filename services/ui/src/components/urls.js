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
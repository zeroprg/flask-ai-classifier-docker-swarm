import React, { useState, useEffect } from 'react';

const ObjectOfInterest = (props) => {
    
    const PAGINATOR = 100

    const popup_image = (event) =>{
        if(event.target.classList.contains('img_thumb')){
            event.target.classList.replace('img_thumb', 'popup');   
        } else if(event.target.classList.contains('popup')){
            event.target.classList.remove('popup', 'img_thumb');    
        }
    }

    //const [selected_obj_of_interest, setObjectOfInterest]  = useState([props.object_of_interest[0]])
 
    const [data, setData]   = useState(null);
    const [counter, setCounter]   = useState(PAGINATOR);

    const {cam} = props;

    async function fetchImageData(objectOfInterest,timerange) {
        const DEFAULT_QUERY =  global.config.API + "moreimgs?start=" + timerange.start + 
        "&cam=" + cam + "&end=" + timerange.end + "&object_of_interest=" + objectOfInterest

        fetch(DEFAULT_QUERY)
            .then(response => {
                // make sure to check for errors
                console.log(" response:" + response)
                if (response.ok) {
                    console.log(" response:" + JSON.stringify(response, null, 2) )
                    return response.json();
                } else {
                    console.log(" error:")
                    throw new Error('Something went wrong ...');
                }
            })
            .then(json => { 
                setData(json)
                setCounter( json.length - 1 );
             });
    }


    useEffect(() => { 
        fetchImageData(props.object_of_interest, props.timerange);
        },
        [props.cam, props.object_of_interest, props.timerange]);
     
    
        
    function removeClass(classname, event){
        let nextSibling = event.target.nextElementSibling;
        while( nextSibling ){
            nextSibling.classList.remove(classname);
            nextSibling = nextSibling.nextElementSibling;
        }
        let prevSibling = event.target.previousElementSibling;
        while( prevSibling ){
            prevSibling.classList.remove(classname);
            prevSibling= prevSibling.previousElementSibling;
        }
    }

    function seek( direction, event) {
        
        if (counter + direction  <  0 ) return;
        if (counter + direction  >  data.length -1 ) return;
        removeClass('outlined', event);

        if (direction === 0 ){
            let nextSibling = event.target.nextElementSibling;
            nextSibling.classList.add('outlined');
            setCounter(counter + direction);
            return;
        }

        if (counter + direction  === 0 ){
            event.target.classList.add('outlined');
            setCounter(counter + direction);
            return;
        }
         if(counter + direction === data.length -1 ){
            event.target.classList.add('outlined');
            setCounter(counter + direction);
            return;
        } 
        
        // common case
        setCounter(counter + direction);

        console.log('counter:'+ counter);

    }
    

    function renderableItems() {
            return data.slice( counter - PAGINATOR , counter);
    }
    


    if (!data) {
        return "loading...";
    }
    
  
    return (
      <span>

        <div id="navigation" className="text-center">
            <button data-testid="button-restart" className="small" onClick = {(e) =>seek(0,e)}>Restart ({data.length - 1})</button>
            <button data-testid="button-prev" className="small outlined" onClick = {(e) =>seek(+PAGINATOR, e)}>Prev ({counter + PAGINATOR })</button>
            <button data-testid="button-next" className="small" onClick = {(e) =>seek(-PAGINATOR, e)}>Next ({counter - PAGINATOR })</button>
        </div>

        <div id={'Objectsfilter'+ props.cam } className="tabcontent" style={{display:'block'}}>
          <div id={'cam'+ props.cam} className="images_row">
           {data.map(data =>
            <img key={data.hashcode} id={data.hashcode} className={'img_thumb'} src={data.frame}  alt={data.currentime} onClick={popup_image.bind(this)} />
           )} 
        </div> 
        </div>                        
       </span>
    );
  }
export default ObjectOfInterest
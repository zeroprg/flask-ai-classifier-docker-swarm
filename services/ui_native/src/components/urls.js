import React, { useState } from 'react';

const URLlist = (props) => {
  const [data, setData] = useState(props.data);

  const buttonClickHide = (arg1, arg2) => {
    let elem = document.getElementById("section" + arg2)
    if (elem) elem.style.display = 'none';
  };

  const updateparams = (param) => {
    props.updateparams(param);
  };

  const updateurls = (data) => {
    setData(data);
    props.updateurls(data);
  };

  const buttonClickShow = (cam) => {
    updateparams({ videoalignment: 'both' });
    let elem = document.getElementById("section" + cam);

    if (elem) {
      elem.scrollIntoView();
    }
  };

  return (
    data && data.length > 0 ?
      <ul>
        {data.map(data =>
          <li key={data.cam}>
            <a href={data.url}>{data.url}</a>
            &nbsp;
            <a onClick={() => buttonClickShow(data.url)} className="btn btn-primary a-btn - slide - text">
              <span className="glyphicon" aria-hidden="true"></span>
              <span>
                <strong>Show</strong>
              </span>
            </a>
          </li>
        )}
      </ul>
      :
      <p className="loading"> ...  Loading ...</p>
  );
}

export default URLlist;

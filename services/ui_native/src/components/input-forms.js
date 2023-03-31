import React, { useState } from 'react';
import axios from 'axios';
import { SnackbarConsumer } from '../snackbarContext';
import t from '../translator';

const InputURL = ({ updateparams }) => {
  const [isLoading, setIsLoading] = useState(false);
  //const [videoalignment, setVideoAlignment] = useState('video');
  const [url, setUrl] = useState('');

  const handleInputChange = (event) => {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    setUrl(value);
    updateparams({ [name]: value });
  };

  const handleClick = (handleOpen) => {
    setIsLoading(true);
    const URL = global.config.API + 'urls';
    const payload = {
      add: url,
    };
    axios
      .post(URL, payload)
      .then(function (response) {
        console.log(response);
        handleOpen(response.data.message, 'success');
      })
      .catch(function (error) {
        console.log(error);
        handleOpen(error.response.data.message, 'error');
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <SnackbarConsumer>
      {({ handleOpen }) => (
        <div>
          {isLoading ? (
            <img alt="" src={'img/fancybox_loading.gif'}></img>
          ) : (
            ''
          )}
          <h3>Enter IP Camera url at this box </h3>
          <h3 style={{ color: '#07ff7f' }}>
            <b dangerouslySetInnerHTML={t('warning')} />
          </h3>
          <div className="form-group">
            <label className="control-label col-sm-2" htmlFor="pwd">
              URL:
            </label>
            <div className="col-sm-12">
              <input
                type="URL"
                className="form-control"
                id="url"
                name="url"
                placeholder={t('enter_url_inbox').__html}
                value={url}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="form-group">
            <div className="col-sm-offset-2 col-sm-12">
              <input
                type="button"
                value="Submit"
                className="btn btn-primary a-btn - slide - text"
                onClick={() => handleClick(handleOpen)}
              />
            </div>
          </div>

          {/*<form id="myform" className="form-horizontal">
              <FormControl component="fieldset">
                  <RadioGroup row aria-label="videoalignment" name="videoalignment" value={videoalignment} onChange={(e) => setVideoAlignment(e.target.value)}>
                      <FormControlLabel value="video" control={<Radio />} label="Show only video" />
                      <FormControlLabel value="statistic" control={<Radio />} label="Show captured objects only" />
                  </RadioGroup>
              </FormControl>                           
          </form>
          */}
        </div>
      )}
    </SnackbarConsumer>
  );
};

export default InputURL;

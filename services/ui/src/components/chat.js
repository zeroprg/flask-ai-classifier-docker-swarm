import React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 150,
    maxWidth: 550,
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: 2,
  },
  noLabel: {
    marginTop: theme.spacing(3),
  },
}));

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};


function getStyles(name, objectName, theme) {
  return {
    fontWeight:
      objectName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

  const SelectObj = (props) => {
    const classes = useStyles();
    const theme = useTheme();
    const [message, setMessage] = React.useState("Hi... ");
    const [messageToSent, setMessageToSent] = React.useState(message);

    const handleChange = (event) => {
        setMessage(event.target.value);
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
          console.log('Enter was clicked');
          setMessageToSent(this.state.message);
       }
    }


    return (
        <div>
        {this.state.isLoading? <p className="loading"> ... Loading </p>:''} 
        <h3>Welcome to our chat  </h3>
        <div>
        <Messages message={this.state.messageToSent}/> 
            <div className="col-sm-10">
             <input className="form-control" id="message" name="message" placeholder="Enter message here"
                     value={this.state.url} onChange={this.handleInputChange} onKeyDown={handleKeyDown}/>
            </div>
        </div>
        </div>
);
}
export default Chat
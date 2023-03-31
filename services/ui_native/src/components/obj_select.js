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
    const [objectName, setObjectName] = React.useState(props.selected_object_of_interest);
    

    const handleChange = (event) => {
      setObjectName(event.target.value);
      props.onParamsChanged(event.target.value);
    };


    return (
      <div>
        <FormControl className={classes.formControl}>
          <InputLabel id="demo-mutiple-name-label">Filter by interest</InputLabel>
          <Select
            labelId="demo-mutiple-name-label"
            id="demo-mutiple-name"
            multiple
            value={objectName}
            onChange={handleChange}
            input={<Input />}
            MenuProps={MenuProps}
          >
            {props.object_of_interest.map((name) => (
              <MenuItem key={name} value={name} style={getStyles(name, objectName, theme)}>
                {name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      
      </div>
    );
}
export default SelectObj
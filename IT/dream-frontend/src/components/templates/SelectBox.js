import PropTypes from 'prop-types';
// material
import { MenuItem, TextField } from '@mui/material';
import React, {useEffect, useState} from "react";

// ----------------------------------------------------------------------

BlogPostsSort.propTypes = {
  options: PropTypes.array,
  onSort: PropTypes.func
};

export default function BlogPostsSort({ options, onSelect, defaultValue="", label="" }) {

  return (
    <TextField label={label} select defaultValue={defaultValue} style={{minWidth:"10rem"}}>
      {options.map((option) => (
        <MenuItem key={option.value} value={option.value} onClick={()=>onSelect(option.value)}>
          {option.label}
        </MenuItem>
      ))}
    </TextField>
  );
}

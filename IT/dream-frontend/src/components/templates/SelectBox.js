import PropTypes from 'prop-types';
// material
import { MenuItem, TextField } from '@mui/material';
import React, {useEffect, useState} from "react";

// ----------------------------------------------------------------------

BlogPostsSort.propTypes = {
  options: PropTypes.array,
  onSort: PropTypes.func
};

export default function BlogPostsSort({ options, onSelect, defaultValue="" }) {

  return (
    <TextField select size="small" defaultValue={defaultValue}>
      {options.map((option) => (
        <MenuItem key={option.value} value={option.value} onClick={()=>onSelect(option.value)}>
          {option.label}
        </MenuItem>
      ))}
    </TextField>
  );
}

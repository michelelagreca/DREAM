import PropTypes from 'prop-types';
// material
import { MenuItem, TextField } from '@mui/material';
import React, {useEffect, useState} from "react";

// ----------------------------------------------------------------------

BlogPostsSort.propTypes = {
  options: PropTypes.array,
  onSort: PropTypes.func
};

export default function BlogPostsSort({ options, onSort, value }) {

  return (
    <TextField select size="small" defaultValue={"Posts"}>
      {options.map((option) => (
        <MenuItem key={option.value} value={option.value} onClick={()=>onSort(option.value)}>
          {option.label}
        </MenuItem>
      ))}
    </TextField>
  );
}

import { Icon } from '@iconify/react';
import React, { useRef, useState } from 'react';
import editFill from '@iconify/icons-eva/bulb-fill';
import { Link as RouterLink } from 'react-router-dom';
import moreVerticalFill from '@iconify/icons-eva/more-vertical-fill';
// material
import {Menu, MenuItem, IconButton, ListItemIcon, ListItemText, Box, Stack} from '@mui/material';
import star from '@iconify/icons-eva/star-fill'
import remove from '@iconify/icons-eva/close-square-fill'
import CircularProgress from "@material-ui/core/CircularProgress";

// ----------------------------------------------------------------------

export default function CircularProgressCenter({isLoading}) {
    return (
        <>
            {isLoading ?
                <Stack mb={5} direction="column" alignItems="center" justifyContent="space-between">
                    <CircularProgress />
                </Stack>
            : null}
        </>
    );
}

import { Icon } from '@iconify/react';
import React, {useEffect, useRef, useState} from 'react';
import homeFill from '@iconify/icons-eva/home-fill';
import personFill from '@iconify/icons-eva/person-fill';
import settings2Fill from '@iconify/icons-eva/settings-2-fill';
import {Link as RouterLink, useNavigate} from 'react-router-dom';
// material
import { alpha } from '@mui/material/styles';
import { Button, Box, Divider, MenuItem, Typography, Avatar, IconButton } from '@mui/material';
// components

import MenuPopover from "../../MenuPopover";
import account from "../../../../_mocks_/account";
import axiosInstance from "../../../../axios";

// ----------------------------------------------------------------------

const MENU_OPTIONS = [
    {
        label: 'Profile',
        icon: personFill,
        linkTo: '#'
    },
    {
        label: 'Settings',
        icon: settings2Fill,
        linkTo: '#'
    }
];

// ----------------------------------------------------------------------

export default function AccountPopover() {
    const anchorRef = useRef(null);
    const navigate = useNavigate()
    const [open, setOpen] = useState(false);
    const [user, setUser] = useState({name:"", email:""})

    const handleOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    // logout press handler
    const handleLogout = (event) => {
        event.preventDefault();

        // add token to the black list causing the user to logout

        axiosInstance.post('user/logout/blacklist/', {
            refresh_token: localStorage.getItem('refresh_token'),
        }).catch((e)=>alert(e));    // add custom error management here if needed

        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        axiosInstance.defaults.headers['Authorization'] = null;
        navigate('/')
    };

    useEffect(()=>{
        axiosInstance
            .get(`user/info/`,)
            .then((res) =>{
                if(res.data[0])
                    setUser({
                        name : res.data[0].first_name + " " + res.data[0].last_name,
                        email : res.data[0].email
                    })
            })
            .catch((e)=>alert(e))
    },[])

    return (
        <>
            <IconButton
                ref={anchorRef}
                onClick={handleOpen}
                sx={{
                    padding: 0,
                    width: 44,
                    height: 44,
                    ...(open && {
                        '&:before': {
                            zIndex: 1,
                            content: "''",
                            width: '100%',
                            height: '100%',
                            borderRadius: '50%',
                            position: 'absolute',
                            bgcolor: (theme) => alpha(theme.palette.grey[900], 0.72)
                        }
                    })
                }}
            >
                <Avatar src={account.photoURL} alt="photoURL" />
            </IconButton>

            <MenuPopover
                open={open}
                onClose={handleClose}
                anchorEl={anchorRef.current}
                sx={{ width: 220 }}
            >
                <Box sx={{ my: 1.5, px: 2.5 }}>
                    <Typography variant="subtitle1" noWrap>
                        {user.name}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                        {user.email}
                    </Typography>
                </Box>

                <Divider sx={{ my: 1 }} />

                {MENU_OPTIONS.map((option) => (
                    <MenuItem
                        key={option.label}
                        to={option.linkTo}
                        component={RouterLink}
                        onClick={handleClose}
                        sx={{ typography: 'body2', py: 1, px: 2.5 }}
                    >
                        <Box
                            component={Icon}
                            icon={option.icon}
                            sx={{
                                mr: 2,
                                width: 24,
                                height: 24
                            }}
                        />

                        {option.label}
                    </MenuItem>
                ))}

                <Box sx={{ p: 2, pt: 1.5 }}>
                    <Button fullWidth color="inherit"
                            variant="outlined"
                            component={RouterLink} to="/"
                            onClick={handleLogout}
                    >
                        Logout
                    </Button>
                </Box>
            </MenuPopover>
        </>
    );
}

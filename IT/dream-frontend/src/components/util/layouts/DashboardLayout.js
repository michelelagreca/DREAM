import React, {useEffect, useState} from 'react';
import { Outlet } from 'react-router-dom';
// material
import { styled } from '@mui/material/styles';
//
import DashboardNavbar from './rootStructure/DashboardNavbar';
import DashboardSidebar from './rootStructure/DashboardSidebar';
import NotificationsPopover from "./rootStructure/NotificationsPopover";

// ----------------------------------------------------------------------

const APP_BAR_MOBILE = 64;
const APP_BAR_DESKTOP = 92;

const RootStyle = styled('div')({
    display: 'flex',
    minHeight: '100%',
    overflow: 'hidden'
});

const MainStyle = styled('div')(({ theme }) => ({
    flexGrow: 1,
    overflow: 'auto',
    minHeight: '100%',
    paddingTop: APP_BAR_MOBILE + 24,
    paddingBottom: theme.spacing(10),
    [theme.breakpoints.up('lg')]: {
        paddingTop: APP_BAR_DESKTOP + 24,
        paddingLeft: theme.spacing(2),
        paddingRight: theme.spacing(2)
    }
}));

// ----------------------------------------------------------------------

export default function DashboardLayout({userType, setUserType}) {
    const [open, setOpen] = useState(false);
    //console.log(userType)
    return (
        <RootStyle>
            <DashboardNavbar userType={userType} onOpenSidebar={() => setOpen(true)} />
            <DashboardSidebar isOpenSidebar={open} onCloseSidebar={() => setOpen(false)} userType={userType}/>
            <MainStyle>
                <Outlet />
            </MainStyle>
        </RootStyle>
    );
}

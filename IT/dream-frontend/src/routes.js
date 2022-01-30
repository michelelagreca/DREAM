import React from "react";
import { Navigate, useRoutes } from 'react-router-dom';
import NotFound from './components/pages/Page404'
import SignUpSecond from "./components/templates/SignUpSecond";
import SignIn from "./components/templates/SignIn";
import Base from "./components/pages/Base"
import SignUpFirst from "./components/templates/SignUpFirst";
import Forum from "./components/pages/Forum";
import FarmersKpis from "./components/pages/FarmersKpis";
import SendHR from "./components/pages/SendHR";
import HrRequests from "./components/templates/HrRequests";
import Logo from "./components/util/Logo";
import TipRequests from "./components/templates/TipRequests";
import HarvestHistory from "./components/templates/HarvestHistory";
import Faq from "./components/templates/FAQ";
import HarvestReport from "./components/templates/harvestReport/HarvestReport";
import {Container, Stack, Typography} from "@mui/material";
import Page from "./components/util/Page";
// layouts



const Dummy = ({title="Work In Progress"}) =>{
    return(
        <Page title="Work In Progress">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                    <Typography variant="h4" gutterBottom>
                        {title}
                    </Typography>

                </Stack>
                <Logo/>
            </Container>
        </Page>
    )
}

// ----------------------------------------------------------------------

export default function Router() {
    return useRoutes([
        { path: '*', element: <Navigate to="/404" replace /> },

        // always redirect just dashboard to dashboard forum
        { path: '/farmer', element: <Navigate to="/farmer/forum" replace />  },
        { path: '/agronomist', element: <Navigate to="/agronomist/forum" replace />  },
        { path: '/policyMaker', element: <Navigate to="/policyMaker/forum" replace />  },
        { path: '/', element: <Navigate to="/forum" replace />  },

        //farmer routes
        {
            path: '/farmer',
            element: <Base isLogoOnlyLayout={false} userTypeInit={"farmer"}/>,
            children: [
                { element: <Navigate to="/farmer/forum" replace /> },
                { path: 'forum', element: <Forum
                        writeQ = {true}
                        writeT = {true}
                        ShowQ = {true}
                        AnswerQ={true}/> },
                { path: 'send-hr', element: <SendHR/> },
                { path: 'faq', element: <Faq/>},
                { path: 'incoming-hr', element: <HrRequests/> },
                { path: 'harvest-rep', element: <HarvestReport/> },
                { path: 'harvest-his', element: /*<HarvestHistory/>*/ <Dummy title={'Harvest History'}/>  },
                { path: 'incoming-tr', element: <TipRequests canModify/> },
                { path: 'visit-messages', element: <Dummy title={'Visit Messages'}/> },
            ]
        },
        //agronomist routes
        {
            path: '/agronomist',
            element: <Base isLogoOnlyLayout={false} userTypeInit={"agronomist"}/>,
            children: [
                { element: <Navigate to="/agronomist/forum" replace /> },
                { path: 'forum', element: <Forum
                        writeT = {true}
                        ShowQ = {true}
                        AnswerQ={true}/> },
                { path: 'incoming-hr', element: <Dummy/> },
                { path: 'faq', element: <Faq/> },
                { path: 'visit-plan', element: <Dummy/> },
                { path: 'visit-messages', element: <Dummy title={'Visit Messages'}/> },
                { path: 'farmers-kpis', element: <FarmersKpis/> },
            ]
        },
        //policy maker routes
        {
            path: '/policyMaker',
            element: <Base isLogoOnlyLayout={false} userTypeInit={"policyMaker"}/>,
            children: [
                { element: <Navigate to="/policyMaker/forum" replace /> },
                { path: 'forum', element: <Forum startT/> },
                { path: 'farmer-kpis', element: <FarmersKpis sendT={true}/> },
                { path: 'send-tr', element: <TipRequests/> },
            ]
        },

        //anonymous user routes
        {
            path: '/',
            element: <Base isLogoOnlyLayout={false} userTypeInit={"anonymous"}/>,
            children: [
                { path: 'login', element: <SignIn/> },
                { path: 'register', element: <SignUpFirst/> },
                { path: 'credentials', element: <SignUpSecond/> },
                { path: 'forum', element: <Forum />},

            ]
        },
        //redirect error routes
        {
            path: '/',
            element: <Base isLogoOnlyLayout={true}/>,
            children: [
                { path: '404', element: <NotFound /> },
                { path: '*', element: <Navigate to="/404" /> }
            ]
        },
    ]);
}

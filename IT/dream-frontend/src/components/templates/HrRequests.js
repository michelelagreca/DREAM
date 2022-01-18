import faker from 'faker';
import PropTypes from 'prop-types';
import { Icon } from '@iconify/react';
import { formatDistance } from 'date-fns';
import { Link as RouterLink } from 'react-router-dom';
import arrowIosForwardFill from '@iconify/icons-eva/arrow-ios-forward-fill';
// material
import {Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, IconButton, Container} from '@mui/material';
// utils

//
import Scrollbar from '../util/Scrollbar';
import {mockImgCover} from "../util/extra/mockImages";
import React, {useState} from "react";
import TipEditorAndChat from "../molecules/TipEditorAndChat";
import HrViewAndChat from "../molecules/HrViewAndChat";
import arrowBack from "@iconify/icons-eva/arrow-back-fill";
import Page from "../util/Page";

const EXAMPLE_CHAT = [
    {writer: 'user', text:'I need help!'},
    {writer: 'extern', text:'I can help you, no worries'},
]

// ----------------------------------------------------------------------

const NEWS = [...Array(5)].map((_, index) => {
    const setIndex = index + 1;
    return {
        title: faker.name.title(),
        description: faker.lorem.paragraphs(),
        image: mockImgCover(setIndex),
        postedAt: faker.date.soon()
    };
});

// ----------------------------------------------------------------------

HrItem.propTypes = {
    news: PropTypes.object.isRequired
};

function HrItem({ news, setSelectedHr }) {
    const { image, title, description, postedAt } = news;
    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // Now send the message throught the backend API
    };
    return (

        <Stack direction="row" alignItems="center" spacing={2}>
            <Box
                component="img"
                alt={title}
                src={image}
                sx={{ width: 48, height: 48, borderRadius: 1.5 }}
            />
            <Box sx={{ minWidth: 240 }}>
                <Link style={{cursor:"pointer"}} color="inherit" underline="hover" onClick={()=>setSelectedHr(news)}>
                    <Typography variant="subtitle2" noWrap>
                        {title}
                    </Typography>
                </Link>
                <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                    {description}
                </Typography>
            </Box>
            <Typography variant="caption" sx={{ pr: 3, flexShrink: 0, color: 'text.secondary' }}>
                {formatDistance(postedAt, new Date())}
            </Typography>
        </Stack>
    );
}

export default function HrRequests() {
    const [selectedHr,setSelectedHr] = useState(null)
    return (
        <Page title="Help Requests">
            <Container>
            <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h4" gutterBottom>
                    Help Requests
                </Typography>

            </Stack>
            {selectedHr ?
                <Stack m={1} direction="row" alignItems="flex-start">
                    <IconButton onClick={() => setSelectedHr(null)}>
                        <Icon icon={arrowBack} width={25} height={25}/>
                    </IconButton>
                </Stack>
                : null
            }
            <Card>
                {selectedHr ? <CardHeader title="Help Request" />:null}
                    {!selectedHr ?
                        <Stack spacing={3} sx={{ p: 3, pr: 0 }}>
                            {NEWS.map((news) => (
                                <HrItem key={news.title} news={news} setSelectedHr={setSelectedHr}/>
                            ))}
                        </Stack>
                        :
                        <HrViewAndChat chat={EXAMPLE_CHAT} item={selectedHr}/>
                    }
            </Card>
            </Container>
        </Page>
    );
}

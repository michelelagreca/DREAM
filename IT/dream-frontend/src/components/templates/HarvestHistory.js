import faker from 'faker';
import PropTypes from 'prop-types';
import { formatDistance } from 'date-fns';
// material
import {Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, IconButton, Container} from '@mui/material';
// utils

//
import Scrollbar from '../util/Scrollbar';
import {mockImgCover} from "../util/extra/mockImages";
import React, {useState} from "react";
import Page from "../util/Page";

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

HarvestItem.propTypes = {
    news: PropTypes.object.isRequired
};

function HarvestItem({ news, setSelectedHr }) {
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
                <Link style={{cursor:"pointer"}} color="inherit" underline="hover">
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

export default function HarvestHistory() {
    return (
        <Page title="Harvest History">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                    <Typography variant="h4" gutterBottom>
                        Harvest History
                    </Typography>

                </Stack>
                <Card>
                    {/*<CardHeader title="Harvest History" />*/}

                    <Stack spacing={3} sx={{ p: 3, pr: 0 }}>
                        {NEWS.map((news) => (
                            <HarvestItem key={news.title} news={news}/>
                        ))}
                    </Stack>

                </Card>
            </Container>
        </Page>
    );
}

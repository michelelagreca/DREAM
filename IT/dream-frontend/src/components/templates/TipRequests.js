import faker from 'faker';
import PropTypes from 'prop-types';
import { Icon } from '@iconify/react';
import { formatDistance } from 'date-fns';
import { Link as RouterLink } from 'react-router-dom';
import arrowBack from '@iconify/icons-eva/arrow-back-fill';
// material
import {Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, Container, IconButton} from '@mui/material';
// utils

//

import React, {useState} from "react";
import {mockImgCover} from "../util/extra/mockImages";
import Scrollbar from "../util/Scrollbar";
import TipEditorAndChat from "../molecules/TipEditorAndChat";
import Page from "../util/Page";
import moreVerticalFill from "@iconify/icons-eva/more-vertical-fill";

// ----------------------------------------------------------------------

const EXAMPLE_CHAT = [
    {writer: 'user', text:'Share some tips!'},
    {writer: 'user', text:'I have seen you are growing amazing crops'},
    {writer: 'extern', text:'Thank you'},
]


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

NewsItem.propTypes = {
    news: PropTypes.object.isRequired
};

function NewsItem({ news, setSelectedItem }) {
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
                <Link style={{cursor:"pointer"}} color="inherit" underline="hover" onClick={()=>setSelectedItem(news)}>
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

export default function TipRequests({canModify=false}) {
    const [selectedTip, setSelectedTip] = useState(null)

    console.log(selectedTip)
    return (
        <Page title="Tip Requests">
            <Container>
            <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h4" gutterBottom>
                    Tip Requests
                </Typography>

            </Stack>
            {selectedTip ?
                <Stack mb={2} direction="row" alignItems="flex-start">
                    <IconButton onClick={() => setSelectedTip(null)}>
                        <Icon icon={arrowBack} width={25} height={25}/>
                    </IconButton>
                </Stack>
                : null
            }
            <Card>

                <CardHeader title="Opened Tip Request" />

                    {!selectedTip ?
                        <Stack spacing={3} sx={{p: 3, pr: 0}}>
                            {NEWS.map((news) => (
                                <NewsItem key={news.title} news={news} setSelectedItem={setSelectedTip}/>
                            ))}
                        </Stack>
                        :
                        <TipEditorAndChat item={selectedTip} chat={EXAMPLE_CHAT} canModify={canModify}/>
                    }

            </Card>
            </Container>
        </Page>
    );
}

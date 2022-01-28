import PropTypes from 'prop-types';
import { Icon } from '@iconify/react';
import { Link as RouterLink } from 'react-router-dom';
import messageCircleFill from '@iconify/icons-eva/message-circle-fill';
import like from '@iconify/icons-eva/arrow-circle-up-fill'
import { styled } from '@mui/material/styles';
import { Box, Link, Card, Grid, Avatar, Typography, CardContent } from '@mui/material';
import {fDate} from "../../extra/formatTime";
import React from "react";
import {fShortenNumber} from "../../extra/formatNumber";
import SvgIconStyle from "../../SvgIconStyle";
import Stack from "@mui/material/Stack";

// ----------------------------------------------------------------------

const CardMediaStyle = styled('div')({
    position: 'relative',
    paddingTop: 'calc(100% * 3 / 4)'
});

const TitleStyle = styled(Link)({
    height: 44,
    overflow: 'hidden',
    WebkitLineClamp: 2,
    display: '-webkit-box',
    WebkitBoxOrient: 'vertical'
});

const InfoStyle = styled('div')(({ theme }) => ({
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'flex-end',
    marginTop: theme.spacing(3),
    color: theme.palette.text.disabled
}));


// ----------------------------------------------------------------------
/*
{   example question
        "id": 1,
        "timestamp": "2022-01-28T00:04:29Z",
        "title": "question 1",
        "text_body": "swwswsws",
        "author_id": 1,
        "category_id": 1,
        "area_id": 1,
        "answers_number": 1
    }
 */

export default function QuestionCard({ post }) {
    const {title, answers_number, timestamp } = post;
    const latestPostLarge = true;  //control large size
    const latestPost = false;   //control medium size

    const POST_INFO = [
        //{ number: 0, icon: like },
        { number: answers_number, icon: messageCircleFill },
    ];

    return (
        <Grid item xs={12} sm={latestPostLarge ? 12 : 6} md={latestPostLarge ? 6 : 3}>
            <Card sx={{ position: 'relative' }}>
                <CardMediaStyle
                    sx={{
                        ...((latestPostLarge || latestPost) && {
                            pt: 'calc(100% * 4 / 3)',
                            '&:after': {
                                top: 0,
                                content: "''",
                                width: '100%',
                                height: '100%',
                                position: 'absolute',
                                //bgcolor:alpha('#EBF8F2', 0.98)
                                //bgcolor: (theme) => alpha(theme.common.white[500], 0.22)
                            }
                        }),
                        ...(latestPostLarge && {
                            pt: {
                                xs: 'calc(40% * 4 / 3)',
                                sm: 'calc(45% * 3 / 4.66)',
                                md: 'calc(60% * 3 / 4.66)',
                                lg: 'calc(60% * 3 / 4.66)'
                            }
                        })
                    }}
                >
                    <SvgIconStyle
                        color="paper"
                        src="/static/icons/shape-avatar.svg"
                        sx={{
                            width: 80,
                            height: 36,
                            zIndex: 9,
                            bottom: -15,
                            position: 'absolute',
                            ...((latestPostLarge || latestPost) && { display: 'none' })
                        }}
                    />


                    {/*<CoverImgStyle alt={title} src={cover} />*/}
                </CardMediaStyle>

                <CardContent
                    sx={{
                        pt: 4,
                        ...((latestPostLarge || latestPost) && {
                            bottom: 0,
                            width: '100%',
                            position: 'absolute',
                        })
                    }}
                >
                    <TitleStyle
                        to="#"
                        color="inherit"
                        variant="subtitle2"
                        underline="hover"
                        component={RouterLink}
                        sx={{
                            ...(latestPostLarge && { typography: 'h5', height: 60 }),
                            ...((latestPostLarge || latestPost) && {
                                color: 'common.black'
                            })
                        }}
                    >
                        {title}
                    </TitleStyle>
                    <Typography
                        gutterBottom
                        variant="caption"
                        sx={{ color: 'text.disabled', display: 'block' }}
                    >
                        {fDate(timestamp)}
                    </Typography>

                    <InfoStyle>
                        <Stack direction={"row"} width={"100%"} justifyContent={"flex-end"}>
                            {POST_INFO.map((info, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        ml: index === 0 ? 0 : 1.5,
                                        ...((latestPostLarge || latestPost) && {
                                            color: 'grey.500'
                                        })
                                    }}
                                >
                                    <Box component={Icon} icon={info.icon} sx={{ width: 20, height: 25, mr: 0.5 }} />
                                    <Typography variant="caption">{fShortenNumber(info.number)}</Typography>
                                </Box>
                            ))}
                        </Stack>
                    </InfoStyle>
                </CardContent>
            </Card>
        </Grid>
    );
}

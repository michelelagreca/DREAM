import { Icon } from '@iconify/react';
import { Link as RouterLink } from 'react-router-dom';
import like from '@iconify/icons-eva/arrow-circle-up-fill'
import star from '@iconify/icons-eva/star-fill'
import { styled } from '@mui/material/styles';
import { Box, Link, Card, Grid, Typography, CardContent } from '@mui/material';
import React, {useState} from "react";
import {fShortenNumber} from "../../extra/formatNumber";
import TipMoreMenu from "../../../molecules/TipMoreMenu";
import Stack from "@mui/material/Stack";
import {fDate} from "../../extra/formatTime";

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

/* example of tip data
    area_id: 1
    author_id: 2
    category_id: 1
    dislikes: 0
    id: 2
    is_star: false
    likes: 1
    text_body: "3344"
    timestamp: "2022-01-27T19:08:01Z"
    title: "33"
    user_dislike: false
    user_like: false
 */

export default function TipCard({ post,starT }) {
    const { is_star, title, likes, dislikes, text_body, timestamp } = post;
    const latestPostLarge = true;  //control large size
    const latestPost = false;   //control medium size
    const [isStar, SetIsStar] = useState(is_star)

    const POST_INFO = [
        { number: likes-dislikes, icon: like},
    ];
    const STAR_INFO = [
        { number: isStar ? 1 : 0, icon: star }, //number == 1  is start
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
                                //bg color here set the card color
                                //bgcolor: (theme) => alpha(theme.palette.grey[900], 0.72)
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
                    <Typography
                        gutterBottom
                        variant="caption"
                        sx={{ color: 'text.disabled', display: 'block' }}
                    >
                        {fDate(timestamp)}
                    </Typography>
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
                    <InfoStyle>
                        <Stack direction={"row"} width={"100%"} justifyContent={"space-between"}>
                            {STAR_INFO.map((info, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        ml: index === 0 ? 0 : 1.5,
                                        ...((latestPostLarge || latestPost) && {
                                            color: 'gold'
                                        })
                                    }}
                                >
                                    {isStar ? <Box component={Icon} icon={info.icon} sx={{ width: 20, height: 25, mr: 0.5 }} /> : null}
                                </Box>
                            ))}
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
                                    {starT ?
                                        //star tip menu
                                        <TipMoreMenu isStar={isStar} setIsStar={SetIsStar}/> : null
                                    }
                                </Box>
                            ))}
                        </Stack>
                    </InfoStyle>
                </CardContent>
            </Card>
        </Grid>
    );
}

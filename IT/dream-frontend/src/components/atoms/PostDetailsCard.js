import { Icon } from '@iconify/react';
import {Link as RouterLink, useNavigate} from 'react-router-dom';
import messageCircleFill from '@iconify/icons-eva/message-circle-fill';
import like from '@iconify/icons-eva/arrow-circle-up-fill'
import { styled } from '@mui/material/styles';
import {Box, Link, Card, Grid, Avatar, Typography, CardContent, IconButton} from '@mui/material';
import Stack from "@mui/material/Stack";
import React from "react";
import {fDate} from "../util/extra/formatTime";
import {fShortenNumber} from "../util/extra/formatNumber";
import SvgIconStyle from "../util/SvgIconStyle";
import AnswerLikeMenu from "../molecules/AnswerLikeMenu";
import star from '@iconify/icons-eva/star-fill'
import axiosInstance from "../../axios";
import arrowBack from "@iconify/icons-eva/arrow-back-fill";

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

export default function PostDetailsCard({post, isTip, setPost, setData}) {
    const {user_like, user_dislike, title, answers_number, timestamp, text_body, likes, dislikes, is_star, id } = post;
    const latestPostLarge = true;  //control large size
    const latestPost = false;   //control medium size
    const up = likes ? likes : 0
    const down = dislikes ? dislikes : 0
    const navigation = useNavigate()

    const handleTipLike = (event) =>{
        const post_obj ={
            tip_id: id,
        }
        axiosInstance
            .post('voting/tip/like', post_obj)
            .then((res) =>{
                let postRefreshed = {...post}
                postRefreshed.likes = postRefreshed.likes + 1
                postRefreshed.user_dislike = false
                postRefreshed.user_like = true
                setPost({isTip:isTip, post:postRefreshed})
            })
            .catch((e)=>alert(e))
    }
    const handleTipDislike = (event) =>{
        const post_obj ={
            tip_id: id,
        }
        axiosInstance
            .post('voting/tip/dislike', post_obj)
            .then((res) =>{
                let postRefreshed = {...post}
                postRefreshed.dislikes = postRefreshed.dislikes + 1
                postRefreshed.user_dislike = true
                postRefreshed.user_like = false
                setPost({isTip:isTip, post:postRefreshed})
            })
            .catch((e)=>alert(e))
    }
    const handleTipRemoveVote = (event) =>{
        const post_obj ={
            tip_id: id,
        }
        axiosInstance
            .post('voting/tip/remove-vote', post_obj)
            .then((res) =>{
                let postRefreshed = {...post}
                if(user_like) {
                    postRefreshed.user_dislike = false
                    postRefreshed.user_like = false
                    postRefreshed.likes = postRefreshed.likes - 1
                    setPost({isTip: isTip, post: postRefreshed})
                }
                else if (user_dislike){
                    postRefreshed.dislikes = postRefreshed.dislikes - 1
                    postRefreshed.user_dislike = false
                    postRefreshed.user_like = false
                    setPost({isTip: isTip, post: postRefreshed})
                }
            })
            .catch((e)=>alert(e))
    }


    return (
        <Grid item xs={12} sm={latestPostLarge ? 12 : 6} md={latestPostLarge ? 8 : 3}>
            <Stack m={1} direction="row" alignItems="flex-start">
                <IconButton onClick={() => {
                    setPost({isTip: isTip})
                    setData({loading: true})
                }}>
                    <Icon icon={arrowBack} width={25} height={25}/>
                </IconButton>
            </Stack>
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
                        color="inherit"
                        variant="subtitle2"
                        underline="hover"
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
                        variant="subtitle1"
                        sx={{ color: 'text.disabled', display: 'block' }}
                    >
                        {text_body}
                    </Typography>
                    <Typography
                        gutterBottom
                        variant="caption"
                        sx={{ color: 'text.disabled', display: 'block' }}
                    >
                        {fDate(timestamp)}
                    </Typography>
                    {isTip ?
                        <InfoStyle>
                            <Stack direction={"row"} width={"100%"} justifyContent={"space-between"}>
                                <Stack>
                                    {is_star ? <Box component={Icon} icon={star}
                                                    sx={{width: 30, height: 35, mr: 0.5, color: "gold"}}/>
                                        : null
                                    }
                                    <Typography variant="caption1">{`Score: ${up - down}`}</Typography>
                                </Stack>
                                <Stack>
                                    <AnswerLikeMenu
                                        handleRemove={handleTipRemoveVote}
                                        handleLike={handleTipLike}
                                        handleDislike={handleTipDislike}
                                        isUserLike={user_like}
                                        isUserDislike={user_dislike}
                                    />
                                </Stack>
                            </Stack>
                        </InfoStyle>
                        : null
                    }
                </CardContent>
            </Card>
        </Grid>
    );
}

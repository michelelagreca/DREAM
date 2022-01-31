import { Icon } from '@iconify/react';
import { formatDistance } from 'date-fns';
import {Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, IconButton, Container} from '@mui/material';
import React, {useEffect, useState} from "react";
import arrowBack from "@iconify/icons-eva/arrow-back-fill";
import CircularProgressCenter from "../molecules/CircularProgressCenter";
import send from '@iconify/icons-eva/upload-fill'
import receive from '@iconify/icons-eva/corner-left-down-fill'
import PostDetailsCard from "../atoms/PostDetailsCard";
import axiosInstance from "../../axios";
import like from "@iconify/icons-eva/arrow-circle-up-fill";
import dislike from "@iconify/icons-eva/arrow-circle-up-fill";
import none from "@iconify/icons-eva/arrow-back-fill";
import AnswerLikeMenu from "./AnswerLikeMenu";

function AnswerItem({ answer, setSelectedHr }) {
    /* answer example
    author_id: 1
    dislikes: 0
    id: 1
    likes: 4
    question_id: 1
    text_body: "This is an answer"
    timestamp: "2022-01-30T11:34:18Z"
    user_dislike: false
    user_like: true
     */
    const { user_like, user_dislike,likes,dislikes, text_body, status, timestamp, is_sender } = answer;
    const up = likes ? likes : 0
    const down = dislikes ? dislikes : 0
    console.log(answer)
    return (

        <Stack direction="column" alignItems="flex-start" spacing={2} justifyContent={"space-between"}>
            <Stack direction="row" alignItems="center">
                <Icon
                    icon={user_like ? like : user_dislike ? dislike : none}
                    sx={{ width: 48, height: 48, borderRadius: 1.5 }}
                />
                <Box sx={{ minWidth: 200, marginLeft:2 }}>
                    <Link style={{cursor:"pointer"}} color="inherit" underline="hover" >
                        <Typography variant="subtitle1" noWrap>
                            {text_body}
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                            {status}
                        </Typography>
                    </Link>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }} noWrap>
                        {new Date(timestamp).toDateString()}
                    </Typography>
                </Box>
            </Stack>
            <Stack style={{width:"100%"}} direction="row" alignItems="center"  justifyContent="space-between">
                <Typography variant="caption" sx={{ pr: 3, flexShrink: 0 }}>
                    {`Score: ${up-down}`}
                </Typography>
                <AnswerLikeMenu/>
            </Stack>

        </Stack>
    );
}

export default function PostDisplayer({isTip, post, setPost}) {
    const [selectedAnswer,setSelectedAnswer] = useState(null)
    const [data, setData] = useState({loading: true})

    //console.log(data)
    // get all answers

    useEffect(()=>{
        if(data.loading && !isTip)
            axiosInstance
                .get(`/reading/answers/`, {params: {id: post.id}})
                .then((res) => {
                    setData({loading: false, answer_list: res.data})
                })
                .catch(e=>alert(e))
    }, [data])

    return (
        <Container>
            <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h4" gutterBottom>
                    Post Details
                </Typography>

            </Stack>

            <Stack m={1} direction="row" alignItems="flex-start">
                <IconButton onClick={() => setPost({isTip:false, data: null})}>
                    <Icon icon={arrowBack} width={25} height={25}/>
                </IconButton>
            </Stack>
            <PostDetailsCard post={post} />
            {!data.loading ?
                <Stack mt={2} >
                    <Card>
                        {/*/selectedHr ? <CardHeader title="Help Request"/> : null*/}
                        {data.answer_list ?
                            <Stack m={2} spacing={3} sx={{p: 3, pr: 0}}>
                                {data.answer_list.map((answer,i) => (
                                    <AnswerItem key={i} answer={answer} />
                                ))}
                            </Stack>
                            :
                            null
                        }
                    </Card>
                </Stack>
                :null}
            <CircularProgressCenter isLoading={data.loading && !isTip} color={'primary'}/>
        </Container>
    );
}

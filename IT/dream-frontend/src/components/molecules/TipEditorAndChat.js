import {IconButton, Stack, TextField, Typography} from "@mui/material";
import Label from "../util/Label";
import React, {useEffect, useState} from 'react';
import { Widget, addResponseMessage,addUserMessage,dropMessages} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import './chat.css';
import Button from "@mui/material/Button";
import {Icon} from "@iconify/react";
import moreVerticalFill from "@iconify/icons-eva/more-vertical-fill";
import axiosInstance from "../../axios";


const TipEditorAndChat = ({item, setData, canModify, setSelectedTip}) =>{
    const [deleteMessages, setDeleteMessages] = useState(0)
    const [chat, setChat] = useState({loading: true, data:[]})
    const [title, setTitle] = useState(item.proposed_title)
    const [tip, setTip] = useState(item.proposed_tip)
    useEffect(()=>{
        console.log('render chat')
        if(chat.loading)
            axiosInstance
                // get messages by id of hr (item is the showed hr)
                .get(`chat/load-tr-messages/`, {params: {id: item.id}})
                .then((res) => {
                    console.log(res.data)
                    setChat({loading: false, data: res.data})
                    res.data.forEach((message)=>{
                        if(message['isFromFarmer'] === !canModify)
                            addUserMessage(message.body)
                        else addResponseMessage(message.body)
                    })
                })
                .catch(e=>alert(e))
    }, [chat])
    useEffect(()=>{
        /*prevent user to write in the chat*/
        dropMessages()
        chat.data.forEach((message)=>{
            if(message['isFromSender'] === item.is_sender)
                addUserMessage(message.body)
            else addResponseMessage(message.body)
        })
    },[deleteMessages])

    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);

        //'body', 'reference_tip'
        const post_obj = {
            reference_tip: item.id,
            body:newMessage,
        }

        axiosInstance
            .post(`chat/send-tr-message/`, post_obj)
            .then((res) =>{
                console.log('message sent')
            })
            .catch((e)=>alert(e))
    };
    const handleNewUserMessageLock = () => {
        const i = deleteMessages % 10 + 1
        setDeleteMessages(i)
    };

    const getCustomLauncher = (text="handleToggle",handleToggle) =>
        <Button style={{alignSelf:"flex-end",marginTop:"1rem", marginRight:"1rem",marginBottom:"0.5rem"}} variant={"contained"} onClick={handleToggle}>{text}</Button>
    const cleanPage = () =>{
        setData({loading:true})
        setSelectedTip(null)
    }

    // ----- Handle TR state change -----
    const handleAccept = () => {
        const post_obj = {
            tr_id: item.id,
            status:'farmer',
            proposed_title:"a",
            proposed_tip:"a"
        }
        axiosInstance
            .post(`request/changing_status_tr/`, post_obj)
            .then((res) =>{
                alert("TR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }
    const handleFinalAccept = () => {
        const post_obj = {
            tr_id: item.id,
            status:'accepted',
            proposed_title:"a",
            proposed_tip:"a"
        }
        axiosInstance
            .post(`request/changing_status_tr/`, post_obj)
            .then((res) =>{
                alert("TR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }
    const handleDecline = () => {
        const post_obj = {
            tr_id: item.id,
            status:'declined',
            proposed_title:"a",
            proposed_tip:"a"
        }
        axiosInstance
            .post(`request/changing_status_tr/`, post_obj)
            .then((res) =>{
                alert("TR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }
    const handleReview = () => {
        const post_obj = {
            tr_id: item.id,
            status:'farmer',
            proposed_title:title,
            proposed_tip:tip
        }
        axiosInstance
            .post(`request/changing_status_tr/`, post_obj)
            .then((res) =>{
                alert("TR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }
    const handleSubmit = () => {
        const post_obj = {
            tr_id: item.id,
            status:'review',
            proposed_title:title,
            proposed_tip:tip
        }
        axiosInstance
            .post(`request/changing_status_tr/`, post_obj)
            .then((res) =>{
                alert("TR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }

    /*
        Possible states TR
       'pending'
       'review'
       'farmer'
       'declined'
       'accepted'
    */

    // -------------------------------
    return(
        <>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Proposed title:'}
                </Typography>
                <TextField
                    onChange={(event)=>setTitle(event.target.value)}
                    disabled={(canModify && item.status === 'review')|| !canModify || item.status === 'declined' || item.status === 'accepted'}
                    value={title}
                />
            </Stack>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Proposed tip:'}
                </Typography>
                <TextField
                    disabled={(canModify && item.status === 'review')|| !canModify || item.status === 'declined' || item.status === 'accepted'}
                    placeholder="Tip content"
                    multiline
                    inputProps={{ maxLength: 250 }}
                    rows={7}
                    value={tip}
                    onChange={(event)=>setTip(event.target.value)}
                />
            </Stack>
            {
                //policy maker case
                !canModify && item.status === 'pending' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" color={"primary"} >
                            {'TR sent to the farmer'}
                        </Typography>
                    </Stack>
                    : !canModify && item.status === 'accepted' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" color={"primary"} >
                            {'This TR has been accepted'}
                        </Typography>
                    </Stack>
                    : !canModify && item.status === 'declined' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" color={"error"}>
                            {'This TR has been declined'}
                        </Typography>
                    </Stack>
                    : !canModify && item.status === 'farmer' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" color={"primary"} >
                            {'This TR can be modified by farmer'}
                        </Typography>
                    </Stack>
                    : !canModify && item.status === 'review' ?
                        <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                            <Button variant={"contained"} onClick={handleFinalAccept}>Accept</Button>
                            <Button variant={"contained"} onClick={handleReview}>Require Changes</Button>
                            <Button color="error" variant={"contained"} onClick={handleDecline}>Decline</Button>
                        </Stack>
                    :null

            }
            {
                //farmer case
                canModify && item.status === 'pending' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                        <Button variant={"contained"} onClick={handleAccept}>Accept</Button>
                        <Button color="error" variant={"contained"} onClick={()=>handleDecline()}>Decline</Button>
                    </Stack>
                    :canModify && item.status === 'farmer' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                        <Button variant={"contained"} onClick={handleSubmit}>Submit Changes</Button>
                        <Button color="error" variant={"contained"} onClick={()=>handleDecline()}>Decline</Button>
                    </Stack>
                    :canModify && item.status === 'review' ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" color={"primary"} >
                            {'This TR in under review'}
                        </Typography>
                    </Stack>
                    : canModify && item.status === 'accepted' ?
                        <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                            <Typography variant="subtitle1" color={"primary"} >
                                {'This TR has been accepted'}
                            </Typography>
                        </Stack>
                    : canModify && item.status === 'declined' ?
                        <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                            <Typography variant="subtitle1" color={"error"}>
                                {'This TR has been declined'}
                            </Typography>
                        </Stack>
                    : null
            }
            {item.status === 'farmer' || item.status === 'review' ?
                <Widget
                    fullScreenMode={false}
                    title="TR Messages"
                    subtitle=""
                    showTimeStamp={false}
                    showCloseButton={true}
                    handleNewUserMessage={handleNewUserMessage}
                    launcher={handleToggle => getCustomLauncher("TR Messages",handleToggle)}
                />: null}
        </>
    )
}
export default TipEditorAndChat

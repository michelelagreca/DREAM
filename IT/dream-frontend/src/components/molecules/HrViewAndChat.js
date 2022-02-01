import { Stack, TextField, Typography} from "@mui/material";
import React, {useEffect, useState} from 'react';
import { Widget, addResponseMessage,addUserMessage,dropMessages} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import './chat.css';
import Button from "@mui/material/Button";
import axiosInstance from "../../axios";


const HrViewAndChat = ({item, setData, setSelectedHr}) =>{
    const [deleteMessages, setDeleteMessages] = useState(0)
    const [chat, setChat] = useState({loading: true, data:[]})

    console.log(chat)
    //TODO post chat
    useEffect(()=>{
        console.log('render chat')
        if(chat.loading)
            axiosInstance
                // get messages by id of hr (item is the showed hr)
                .get(`chat/load-hr-messages/`, {params: {id: item.id}})
                .then((res) => {
                    setChat({loading: false, data: res.data})
                    res.data.forEach((message)=>{
                        if(message['isFromSender'] === item.is_sender)
                            addUserMessage(message.body)
                        else addResponseMessage(message.body)
                    })
                })
                .catch(e=>alert(e))
    }, [chat])

    /*prevent user to write in the chat*/
    useEffect(()=>{
        dropMessages()
        chat.data.forEach((message)=>{
            if(message['isFromSender'] === item.is_sender)
                addUserMessage(message.body)
            else addResponseMessage(message.body)
        })
    },[deleteMessages])

    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);

        //'body', 'reference_hr'
        const post_obj = {
            reference_hr: item.id,
            body:newMessage,
        }

        axiosInstance
            .post(`chat/send-hr-message/`, post_obj)
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
        setSelectedHr(null)
    }

    const handleAccept = () => {
        const post_obj = {
            hr_id: item.id,
            status:'accepted'
        }
        console.log(post_obj)
        axiosInstance
            .post(`request/changing_status_hr_farmer/`, post_obj)
            .then((res) =>{
                alert("HR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }

    const handleDecline = () => {
        const post_obj = {
            hr_id: item.id,
            status:'declined'
        }
        console.log(post_obj)
        axiosInstance
            .post(`request/changing_status_hr_farmer/`, post_obj)
            .then((res) =>{
                alert("HR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }

    const handleClose = () => {
        const post_obj = {
            hr_id: item.id,
            status:'closed'
        }
        console.log(post_obj)
        axiosInstance
            .post(`request/changing_status_hr_farmer/`, post_obj)
            .then((res) =>{
                alert("HR status correctly updated")
                cleanPage()
            })
            .catch((e)=>alert(e))
    }

    return(
        <div>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Title:'}
                </Typography>
                <TextField
                    disabled={true}
                    value={item ? item.title : ""}
                />
            </Stack>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Status:'}
                </Typography>
                <TextField
                    disabled={true}
                    value={item ? item.status : ""}
                />
            </Stack>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Request:'}
                </Typography>
                <TextField
                    disabled={true}
                    placeholder="Request content"
                    multiline
                    rows={7}
                    defaultValue={item ? item.content : ""}
                />
            </Stack>
            {item.status === 'not_accepted' && !item.is_sender ?
                <Stack spacing={1} sx={{p: 3, pr: 0}}>
                    <Button variant={"contained"} onClick={handleAccept}>Accept</Button>
                    <Button color="error" variant={"contained"} onClick={handleDecline}>Decline</Button>
                    {/*<Button color="error" variant={"contained"} onClick={()=>{
                        setIsAccepted(false)
                        setIsClose(true)
                    }}>Decline</Button>*/}
                </Stack>
                :item.status === 'not_accepted' && item.is_sender ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" >
                            {'This HR is pending, the other farmer need to accept'}
                        </Typography>
                    </Stack>
                : item.status === 'accepted' ?
                    <Stack spacing={1} sx={{p: 3, pr: 0}}>
                        <Button color="error" variant={"contained"} onClick={handleClose}>Close HR</Button>
                    </Stack>
                    : item.status === 'closed' ?
                        <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                            <Typography variant="subtitle1" color={"error"}>
                                {'This HR is closed'}
                            </Typography>
                        </Stack>
                        :
                        <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                            <Typography variant="subtitle1" color={"error"}>
                                {'This HR has been declined'}
                            </Typography>
                        </Stack>
            }
            {item.status === 'accepted' ?
                <Widget
                    fullScreenMode={false}
                    title="HR Messages"
                    subtitle=""
                    showTimeStamp={false}
                    showCloseButton={true}
                    handleNewUserMessage={handleNewUserMessage}
                    launcher={handleToggle => getCustomLauncher("HR Messages",handleToggle)}
                />
                : item.status === 'closed' ?
                    <Widget
                        fullScreenMode={false}
                        title="HR Messages History"
                        subtitle=""
                        showTimeStamp={false}
                        showCloseButton={true}
                        handleNewUserMessage={handleNewUserMessageLock}
                        launcher={handleToggle => getCustomLauncher("Message History",handleToggle)}
                    />
                    : null
            }
        </div>
    )
}
export default HrViewAndChat
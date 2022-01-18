import {IconButton, Stack, TextField, Typography} from "@mui/material";
import Label from "../util/Label";
import React, {useEffect, useState} from 'react';
import { Widget, addResponseMessage,addUserMessage,dropMessages} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import './chat.css';
import Button from "@mui/material/Button";
import {Icon} from "@iconify/react";
import moreVerticalFill from "@iconify/icons-eva/more-vertical-fill";


const HrViewAndChat = ({item, chat, isAcceptedInit=false, isCloseInit=false}) =>{
    const [isClose, setIsClose] = useState(isCloseInit)
    const [isAccepted, setIsAccepted] = useState(isAcceptedInit)
    const [deleteMessages, setDeleteMEssages] = useState(0)

    useEffect(()=>{
        dropMessages()
        chat.forEach((message)=>{
            if(message["writer"] === 'user')
                addUserMessage(message.text)
            else addResponseMessage(message.text)
        })
    },[])
    useEffect(()=>{
        dropMessages()
        chat.forEach((message)=>{
            if(message["writer"] === 'user')
                addUserMessage(message.text)
            else addResponseMessage(message.text)
        })
    },[deleteMessages])

    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // Now send the message throught the backend API
    };
    const handleNewUserMessageLock = () => {
        const i = deleteMessages % 10 + 1
        setDeleteMEssages(i)
    };
    const getCustomLauncher = (text="handleToggle",handleToggle) =>
        <Button style={{alignSelf:"flex-end",marginTop:"1rem", marginRight:"1rem",marginBottom:"0.5rem"}} variant={"contained"} onClick={handleToggle}>{text}</Button>
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
                    {'Request:'}
                </Typography>
                <TextField
                    disabled={true}
                    placeholder="MultiLine with rows: 2 and rowsMax: 4"
                    multiline
                    rows={5}
                    maxRows={7}
                />
            </Stack>
            {!isAccepted  && !isClose?
                <Stack spacing={1} sx={{p: 3, pr: 0}}>
                    <Button variant={"contained"} onClick={()=>setIsAccepted(true)}>Accept</Button>
                    <Button color="error" variant={"contained"} onClick={()=>{
                        setIsAccepted(false)
                        setIsClose(true)
                    }}>Decline</Button>
                </Stack>
                : !isClose ?
                    <Stack spacing={1} sx={{p: 3, pr: 0}}>
                        <Button color="error" variant={"contained"} onClick={()=>{
                            setIsClose(true)
                        }}>Close HR</Button>
                    </Stack>
                    : isAccepted ?
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
            {isAccepted && !isClose?
                <Widget
                    fullScreenMode={false}
                    title="HR Messages"
                    subtitle=""
                    showTimeStamp={false}
                    showCloseButton={true}
                    handleNewUserMessage={handleNewUserMessage}
                    launcher={handleToggle => getCustomLauncher("HR Messages",handleToggle)}
                />
                : isAccepted && isClose ?
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
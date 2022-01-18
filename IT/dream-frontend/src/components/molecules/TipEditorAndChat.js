import {IconButton, Stack, TextField, Typography} from "@mui/material";
import Label from "../util/Label";
import React, {useEffect, useState} from 'react';
import { Widget, addResponseMessage,addUserMessage,dropMessages} from 'react-chat-widget';
import 'react-chat-widget/lib/styles.css';
import './chat.css';
import Button from "@mui/material/Button";
import {Icon} from "@iconify/react";
import moreVerticalFill from "@iconify/icons-eva/more-vertical-fill";


const TipEditorAndChat = ({item, chat, canModify}) =>{
    const [isAccepted, setIsAccepted] = useState(false)
    const [isDeclined, setIsDeclined] = useState(false)
    useEffect(()=>{
        dropMessages()
        chat.forEach((message)=>{
            if(message["writer"] === 'user')
                addUserMessage(message.text)
            else addResponseMessage(message.text)
        })
    },[])
    const handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // Now send the message throught the backend API
    };
    const getCustomLauncher = (handleToggle) =>
        <Button style={{alignSelf:"flex-end",marginTop:"1rem", marginRight:"1rem",marginBottom:"0.5rem"}} variant={"contained"} onClick={handleToggle}>Toggle Chat</Button>
    return(
        <>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Proposed title:'}
                </Typography>
                <TextField
                    disabled={!canModify}
                    value={item ? item.title : ""}
                />
            </Stack>
            <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                <Typography variant="subtitle3" >
                    {'Proposed tip:'}
                </Typography>
                <TextField
                    disabled={!canModify}
                    placeholder="MultiLine with rows: 2 and rowsMax: 4"
                    multiline
                    rows={5}
                    maxRows={7}
                />
            </Stack>
            {
                //policy maker case
                !canModify && !isAccepted && !isDeclined ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                        <Button variant={"contained"} onClick={()=>setIsAccepted(true)}>Accept</Button>
                        <Button color="error" variant={"contained"} onClick={()=>setIsDeclined(true)}>Decline</Button>
                        <Widget
                            fullScreenMode={false}
                            title="Tip Request Messages"
                            subtitle=""
                            showTimeStamp={false}
                            showCloseButton={true}
                            handleNewUserMessage={handleNewUserMessage}
                            launcher={handleToggle => getCustomLauncher(handleToggle)}
                        />
                    </Stack>
                    : isAccepted ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                        <Typography variant="subtitle1" color={"error"}>
                            {'This TR has been accepted'}
                        </Typography>
                    </Stack>
                    : isDeclined ?
                        <Stack spacing={1} sx={{ p: 3, pr: 0 , alignItems:"center"}} >
                            <Typography variant="subtitle1" color={"error"}>
                                {'This TR has been declined'}
                            </Typography>
                        </Stack> : null
            }
            {
                //farmer case
                canModify && !isAccepted && !isDeclined ?
                    <Stack spacing={1} sx={{ p: 3, pr: 0 }}>
                        <Button variant={"contained"}>Submit Changes</Button>
                        <Button color="error" variant={"contained"} onClick={()=>setIsDeclined(true)}>Decline</Button>
                        <Widget
                            fullScreenMode={false}
                            title="Tip Request Messages"
                            subtitle=""
                            showTimeStamp={false}
                            showCloseButton={true}
                            handleNewUserMessage={handleNewUserMessage}
                            launcher={handleToggle => getCustomLauncher(handleToggle)}
                        />
                    </Stack>
                     : null
            }
        </>
    )
}
export default TipEditorAndChat
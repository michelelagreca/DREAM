import { Icon } from '@iconify/react';
import { formatDistance } from 'date-fns';
import arrowBack from '@iconify/icons-eva/arrow-back-fill';
import {Box, Stack, Link, Card,Typography, CardHeader, Container, IconButton} from '@mui/material';
import React, {useEffect, useState} from "react";
import TipEditorAndChat from "../molecules/TipEditorAndChat";
import Page from "../util/Page";
import send from "@iconify/icons-eva/upload-fill";
import receive from "@iconify/icons-eva/corner-left-down-fill";
import axiosInstance from "../../axios";
import CircularProgressCenter from "../molecules/CircularProgressCenter";


function TrItem({ tr, setSelectedTr, isPolicyMaker }) {
    const { proposed_title, proposed_tip, timestamp, status} = tr;
    return (
        <Stack direction="row" alignItems="center" spacing={2} justifyContent={"space-between"}>
            <Stack direction="row" alignItems="center">
                <Icon
                    icon={isPolicyMaker ? send : receive}
                    sx={{ width: 48, height: 48, borderRadius: 1.5 }}
                />
                <Box sx={{ minWidth: 200, marginLeft:2 }}>
                    <Link style={{cursor:"pointer"}} color="inherit" underline="hover" onClick={()=>setSelectedTr(tr)}>
                        <Typography variant="subtitle1" noWrap>
                            {proposed_title}
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
            <Typography variant="caption" sx={{ pr: 3, flexShrink: 0, color: 'text.secondary' }}>
                {formatDistance(new Date(timestamp), new Date())}
            </Typography>
        </Stack>
    );
}

export default function TipRequests({canModify=false}) {
    const [selectedTip, setSelectedTip] = useState(null)
    const [data, setData] = useState({loading: true})

    console.log(selectedTip)
    console.log(data)
    // get tr requests
    useEffect(()=>{
        if(data.loading)
            if(!canModify)
                axiosInstance
                    .get('request/all_tr_policymaker/')
                    .then((res) => {
                        setData({loading: false, tr_list: res.data})
                    })
                    .catch(e=>alert(e))
            else
                axiosInstance
                    .get('request/all_tr_farmer/')
                    .then((res) => {
                        setData({loading: false, tr_list: res.data})
                    })
                    .catch(e=>alert(e))
    }, [data])

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
                <CircularProgressCenter isLoading={data.loading} color={'primary'}/>
                {!data.loading ?
                    <Card>
                        <CardHeader title="Opened Tip Request" />

                        {!selectedTip ?
                            <Stack spacing={3} sx={{p: 3, pr: 0}}>
                                {data.tr_list.map((tr,i) => (
                                    <TrItem key={i} tr={tr} setSelectedTr={setSelectedTip} isPolicyMaker={!canModify}/>
                                ))}
                            </Stack>
                            :
                            <TipEditorAndChat item={selectedTip} canModify={canModify} setData={setData} setSelectedTip={setSelectedTip}/>
                        }
                    </Card>
                    :null}
            </Container>
        </Page>
    );
}

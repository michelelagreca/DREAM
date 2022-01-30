import PropTypes from 'prop-types';
import { Icon } from '@iconify/react';
import { formatDistance } from 'date-fns';
import {Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, IconButton, Container} from '@mui/material';
import React, {useEffect, useState} from "react";
import HrViewAndChat from "../molecules/HrViewAndChat";
import arrowBack from "@iconify/icons-eva/arrow-back-fill";
import Page from "../util/Page";
import axiosInstance from "../../axios";
import CircularProgressCenter from "../molecules/CircularProgressCenter";
import send from '@iconify/icons-eva/upload-fill'
import receive from '@iconify/icons-eva/corner-left-down-fill'

function HrItem({ hr, setSelectedHr }) {
    const { content, title, status, timestamp, is_sender } = hr;
    return (

        <Stack direction="row" alignItems="center" spacing={2} justifyContent={"space-between"}>
            <Stack direction="row" alignItems="center">
            <Icon
                icon={is_sender ? send : receive}
                sx={{ width: 48, height: 48, borderRadius: 1.5 }}
            />
            <Box sx={{ minWidth: 200, marginLeft:2 }}>
                <Link style={{cursor:"pointer"}} color="inherit" underline="hover" onClick={()=>setSelectedHr(hr)}>
                    <Typography variant="subtitle1" noWrap>
                        {title}
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

export default function HrRequests() {
    const [selectedHr,setSelectedHr] = useState(null)
    const [data, setData] = useState({loading: true})

    //console.log(data)
    // get hr requests
    useEffect(()=>{
        if(data.loading)
            axiosInstance
                .get(`request/all_hr/`)
                .then((res) => {
                    setData({loading: false, hr_list: res.data})
                })
                .catch(e=>alert(e))
    }, [data])

    return (
        <Page title="Help Requests">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                    <Typography variant="h4" gutterBottom>
                        Help Requests
                    </Typography>

                </Stack>
                {selectedHr ?
                    <Stack m={1} direction="row" alignItems="flex-start">
                        <IconButton onClick={() => setSelectedHr(null)}>
                            <Icon icon={arrowBack} width={25} height={25}/>
                        </IconButton>
                    </Stack>
                    : null
                }
                <CircularProgressCenter isLoading={data.loading} color={'primary'}/>
                {!data.loading ?
                    <Card>
                        {selectedHr ? <CardHeader title="Help Request"/> : null}
                        {!selectedHr ?
                            <Stack spacing={3} sx={{p: 3, pr: 0}}>
                                {data.hr_list.map((hr,i) => (
                                    <HrItem key={i} hr={hr} setSelectedHr={setSelectedHr}/>
                                ))}
                            </Stack>
                            :
                            <HrViewAndChat item={selectedHr} setData={setData} setSelectedHr={setSelectedHr}/>
                        }
                    </Card>
                    :null}
            </Container>
        </Page>
    );
}

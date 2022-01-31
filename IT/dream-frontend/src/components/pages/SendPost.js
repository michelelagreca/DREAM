import { Icon } from '@iconify/react';
import sendFIll from '@iconify/icons-eva/corner-left-up-outline'
import {Link as RouterLink, useNavigate} from 'react-router-dom';
import {Grid, Button, Container, Stack, Typography, TextField, TextareaAutosize, MenuItem} from '@mui/material';
import Page from "../util/Page";
import React, {useEffect, useState} from "react";
import axiosInstance from "../../axios";
import SelectBox from "../templates/SelectBox";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";


// ----------------------------------------------------------------------


// ----------------------------------------------------------------------

export default function SendPost({type}) {
    const [form, setForm] = useState({title:"", text_body:""})
    const [category, setCategory] = useState(null)
    const [catList, setCatList] = useState({loading:true, categories:[]})
    const navigation = useNavigate()

    useEffect(()=>{
        axiosInstance
            .get(`categories`)
            .then((res) => {
                setCatList({loading: false, categories: res.data})
            })
            .catch(e=>alert(e))
    },[])

    const handleChangeCategory = (event) => {
        setCategory(event.target.value);
    };

    const handleSend = () =>{
        if (!form.title){
            alert("Title is mandatory")
            return
        }
        if (!form.text_body){
            alert("Content is mandatory")
            return
        }
        if (!category){
            alert("Category is mandatory")
            return
        }

        const post_obj = {
            category: category,
            ...form
        }
        //console.log(post_obj)
        if(type === 'tip')
            axiosInstance
                .post(`posting/tip/`, post_obj)
                .then((res) =>{
                    alert("Tip posted")
                    navigation('/forum')
                })
                .catch((e)=>alert(e))

        else if(type === 'question')
            axiosInstance
                .post(`posting/question/`, post_obj)
                .then((res) =>{
                    alert("Question posted")
                    navigation('/forum')
                })
                .catch((e)=>alert(e))
    }

    return (
        <Page title={type === "tip" ? "New Tip" : "New Question"}>
            <Container>
                <Stack direction="row" alignItems="flex-start" justifyContent="space-between" mb={5}>
                    <Typography variant="h4" gutterBottom>
                        {type === "tip" ? "New Tip" : "New Question"}
                    </Typography>
                </Stack>
                <Stack style={{width:"100%", marginBottom:"2rem"}}>
                    <TextField
                        placeholder="Title"
                        rows={1}
                        onChange={(event) => {
                            setForm({
                                title: event.target.value,
                                text_body: form.text_body
                            })
                        }}
                    />
                </Stack>
                <Stack mb={5} direction="row" alignItems="center" justifyContent="space-between">
                    {/*<BlogPostsSearch posts={POSTS} />*/}
                    {!catList.loading ?
                        <FormControl fullWidth>
                            <TextField
                                select
                                value={category}
                                label="Category"
                                onChange={handleChangeCategory}
                                style={{minWidth:"10rem"}}
                            >
                                {catList.categories.map((option, i) => (
                                    <MenuItem key={i} value={option.name} onClick={()=>setCategory(option.name)}>
                                        {option.name}
                                    </MenuItem>
                                ))}
                            </TextField>
                        </FormControl>
                        : null
                    }
                </Stack>
                <Stack style={{width:"100%", marginBottom:"2rem"}}>
                    <TextField
                        placeholder="Content"
                        multiline
                        rows={5}
                        onChange={(event) => {
                            setForm({
                                title: form.title,
                                text_body: event.target.value
                            })
                        }}
                    />
                </Stack>
                <Stack direction="column" alignItems="flex-end">
                    <Button
                        variant="contained"
                        component={RouterLink}
                        to="#"
                        startIcon={<Icon icon={sendFIll} />}
                        onClick={handleSend}
                    >
                        Publish
                    </Button>
                </Stack>
            </Container>
        </Page>
    );
}

import { Icon } from '@iconify/react';
import plusFill from '@iconify/icons-eva/plus-fill';
import sendFIll from '@iconify/icons-eva/paper-plane-fill'
import { Link as RouterLink } from 'react-router-dom';
// material
import { Grid, Button, Container, Stack, Typography, TextField, TextareaAutosize } from '@mui/material';
// components
import Page from "../util/Page";
import { QuestionCard,TipCard, BlogPostsSort, BlogPostsSearch } from '../../components/util/_dashboard/blog';
//
import POSTS from '../.././_mocks_/blog';
import React, {useState} from "react";
import { useFormik } from 'formik';
import {ProductFilterSidebar} from "../util/_dashboard/products";
import SelectBox from "../templates/SelectBox";
import {TextFields} from "@mui/icons-material";
import axiosInstance from "../../axios";


// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: 'agronomist', label: 'Send to zone Agronomist' },
  { value: 'farmer', label: 'Send to close Farmers' },
];

// ----------------------------------------------------------------------

export default function SendHR({writeQ = false, writeT = false, ShowQ = false,AnswerQ=false}) {
  const [hrType, setHrType] = useState(SORT_OPTIONS[0].value)
  const [form, setForm] = useState({title:"", content:""})

  const handleSend = () =>{
    // soft validation
    if (hrType === SORT_OPTIONS[0].value){
      alert("This functionality will be available soon")
      return
    }
    if (!form.title){
      alert("Title is mandatory")
      return
    }
    if (!form.content){
      alert("Content is mandatory")
      return
    }

    const post_obj = {
      ...form
    }
    //console.log(post_obj)
    axiosInstance
        .post(`request/sending_hr_farmer/`, post_obj)
        .then((res) =>{
          alert("HR correctly sent")
          console.log(res)
          //navigation('/login')
        })
        .catch((e)=>alert(e))
  }
  return (
      <Page title="Send HR">
        <Container>
          <Stack direction="row" alignItems="flex-start" justifyContent="space-between" mb={5}>
            <Typography variant="h4" gutterBottom>
              Send Help Request
            </Typography>
          </Stack>

          <Stack mb={5} direction="row" alignItems="center" justifyContent="space-between">
            {/*<BlogPostsSearch posts={POSTS} />*/}
            <SelectBox options={SORT_OPTIONS} onSelect={setHrType} value={hrType} defaultValue={SORT_OPTIONS[0].value}/>
          </Stack>
          <Stack style={{width:"100%", marginBottom:"2rem"}}>
            <TextField
                placeholder="Title"
                rows={1}
                onChange={(event) => {
                  setForm({
                    title: event.target.value,
                    content: form.content
                  })
                }}
            />
          </Stack>
          <Stack style={{width:"100%", marginBottom:"2rem"}}>
            <TextField
                placeholder="Content"
                multiline
                rows={5}
                onChange={(event) => {
                  setForm({
                    title: form.title,
                    content: event.target.value
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
              Send
            </Button>
          </Stack>
        </Container>
      </Page>
  );
}

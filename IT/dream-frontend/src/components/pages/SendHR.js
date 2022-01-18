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


// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: 'agronomist', label: 'Send to zone Agronomist' },
  { value: 'farmer', label: 'Send to close Farmers' },
];

// ----------------------------------------------------------------------

export default function SendHR({writeQ = false, writeT = false, ShowQ = false,AnswerQ=false}) {
  const [hrType, setHrType] = useState(SORT_OPTIONS[0].value)

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
                placeholder="MultiLine with rows: 2 and rowsMax: 4"
                multiline
                rows={5}
                maxRows={7}
            />
          </Stack>
          <Stack direction="column" alignItems="flex-end">
            <Button
                variant="contained"
                component={RouterLink}
                to="#"
                startIcon={<Icon icon={sendFIll} />}
            >
              Send
            </Button>
          </Stack>
        </Container>
      </Page>
  );
}

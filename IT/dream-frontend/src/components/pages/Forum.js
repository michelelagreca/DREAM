import { Icon } from '@iconify/react';
import plusFill from '@iconify/icons-eva/plus-fill';
import { Link as RouterLink } from 'react-router-dom';
import { Grid, Button, Container, Stack, Typography } from '@mui/material';
import Page from "../util/Page";
import { QuestionCard, TipCard, BlogPostsSort} from '../../components/util/_dashboard/blog';
import React, {useEffect, useState} from "react";
import { useFormik } from 'formik';
import {ProductFilterSidebar} from "../util/_dashboard/products";
import CircularProgressCenter from "../molecules/CircularProgressCenter";
import axiosInstance from "../../axios";


// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: 'Posts', label: 'Questions' },
  { value: 'Tips', label: 'Tips' },
];

// ----------------------------------------------------------------------

export default function Forum({writeQ = false, writeT = false, ShowQ = false,AnswerQ=false, startT=false}) {
  const [postType, setPostType] = useState(SORT_OPTIONS[0].value)
  const [openFilter, setOpenFilter] = useState(false);
  const [data, setData] = useState({loading: true})

  const formik = useFormik({
    initialValues: {
      gender: '',
      category: '',
      colors: '',
      priceRange: '',
      rating: ''
    },
    onSubmit: () => {
      setOpenFilter(false);
    }
  });

  useEffect(()=>{
    // post request to login
    let questions = []
    let tips = []
    axiosInstance
        .get(`reading/tips`)
        .then((res) => {
          if(res)
            tips = res.data ? res.data : tips
        })
        .then(()=>{
          axiosInstance
              .get(`reading/questions`)
              .then((res) => {
                if(res)
                  questions = res.data ? res.data : questions
              })
              .then(()=>{
                setData({loading: false, questions: questions, tips: tips})
              })
        })
        .catch(e=>alert(e))
  }, [])

  const { resetForm, handleSubmit } = formik;

  const handleOpenFilter = () => {
    setOpenFilter(true);
  };

  const handleCloseFilter = () => {
    setOpenFilter(false);
  };

  const handleResetFilter = () => {
    handleSubmit();
    resetForm();
  };

  return (
      <Page title="Dashboard: Forum | Minimal-UI">
        <Container>
          <Stack direction="row" alignItems="flex-start" justifyContent="space-between" mb={5}>
            <Typography variant="h4" gutterBottom>
              Forum
            </Typography>
            <Stack direction="column" alignItems="flex-end" spacing={1} justifyContent="space-between" mb={5}>
              {writeQ ?
                  <Button
                      variant="contained"
                      component={RouterLink}
                      to="#"
                      startIcon={<Icon icon={plusFill} />}
                  >
                    New Question
                  </Button> : null}
              {writeT ?
                  <Button
                      variant="contained"
                      component={RouterLink}
                      to="#"
                      startIcon={<Icon icon={plusFill} />}
                  >
                    New Tip
                  </Button> : null}
            </Stack>
          </Stack>

          <Stack mb={5} direction="row" alignItems="center" justifyContent="space-between">
            {/*<BlogPostsSearch posts={POSTS} />*/}
            <ProductFilterSidebar
                writeQ={writeQ}
                writeT={writeT}
                formik={formik}
                isOpenFilter={openFilter}
                onResetFilter={handleResetFilter}
                onOpenFilter={handleOpenFilter}
                onCloseFilter={handleCloseFilter}
            />
            <BlogPostsSort options={SORT_OPTIONS} onSort={setPostType} value={postType}/>
          </Stack>
          <CircularProgressCenter isLoading={data.loading}/>
          {!data.loading ?
              <Grid container spacing={3}>
                {postType === 'Posts' ?
                    data.questions.map((post, index) => (
                        <QuestionCard key={post.id} post={post} index={index}/>
                    ))
                    :
                    data.tips.map((post, index) => (
                        <TipCard key={post.id} post={post} index={index} starT={startT}/>
                    ))
                }
              </Grid>
              : null}
        </Container>
      </Page>
  );
}

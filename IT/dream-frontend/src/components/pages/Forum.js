import { Icon } from '@iconify/react';
import plusFill from '@iconify/icons-eva/plus-fill';
import { Link as RouterLink } from 'react-router-dom';
// material
import { Grid, Button, Container, Stack, Typography } from '@mui/material';
// components
import Page from "../util/Page";
import { QuestionCard,TipCard, BlogPostsSort, BlogPostsSearch } from '../../components/util/_dashboard/blog';
//
import POSTS from '../.././_mocks_/blog';
import React, {useState} from "react";
import { useFormik } from 'formik';
import {ProductFilterSidebar} from "../util/_dashboard/products";
import CircularProgress from "@material-ui/core/CircularProgress";
import CircularProgressCenter from "../molecules/CircularProgressCenter";


// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: 'Posts', label: 'Questions' },
  { value: 'Tips', label: 'Tips' },
];

// ----------------------------------------------------------------------

export default function Forum({writeQ = false, writeT = false, ShowQ = false,AnswerQ=false, startT=false}) {
  const [postType, setPostType] = useState(SORT_OPTIONS[0].value)
  const [openFilter, setOpenFilter] = useState(false);

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
          <CircularProgressCenter isLoading={true}/>
          <Grid container spacing={3}>
            {postType === 'Posts' ?
                POSTS.map((post, index) => (
                      <QuestionCard key={post.id} post={post} index={index} />
                  ))
                  :
                POSTS.map((post, index) => (
                      <TipCard key={post.id} post={post} index={index} starT={startT}/>
                  ))
            }
          </Grid>
        </Container>
      </Page>
  );
}

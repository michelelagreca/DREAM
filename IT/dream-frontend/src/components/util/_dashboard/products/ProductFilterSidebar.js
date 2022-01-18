import PropTypes from 'prop-types';
import { Icon } from '@iconify/react';
import { Form, FormikProvider } from 'formik';
import closeFill from '@iconify/icons-eva/close-fill';
import roundClearAll from '@iconify/icons-ic/round-clear-all';
import roundFilterList from '@iconify/icons-ic/round-filter-list';
// material
import {
  Box,
  Radio,
  Stack,
  Button,
  Drawer,
  Rating,
  Divider,
  Checkbox,
  FormGroup,
  IconButton,
  Typography,
  RadioGroup,
  FormControlLabel
} from '@mui/material';
import Scrollbar from "../../Scrollbar";

//

// ----------------------------------------------------------------------

export const FILTER_GENDER_OPTIONS = ['Men', 'Women', 'Kids'];
export const FILTER_CATEGORY_OPTIONS = ['Category1', 'Category2', 'Category3', 'Category4'];
export const FILTER_RATING_OPTIONS = ['up4Star', 'up3Star', 'up2Star', 'up1Star'];
export const FILTER_PRICE_OPTIONS = [
  { value: 'All', label: 'All' },
  { value: 'Zone1', label: 'Zone1' },
  { value: 'Zone2', label: 'Zone2' },
  { value: 'Zone3', label: 'Zone3' }
];
export const FILTER_AUTHOR_OPTIONS = [
  { value: 'Me', label: 'Me' },
  { value: 'All', label: 'All' },

];
export const FILTER_COLOR_OPTIONS = [
  '#00AB55',
  '#000000',
  '#FFFFFF',
  '#FFC0CB',
  '#FF4842',
  '#1890FF',
  '#94D82D',
  '#FFC107'
];

// ----------------------------------------------------------------------

ShopFilterSidebar.propTypes = {
  isOpenFilter: PropTypes.bool,
  onResetFilter: PropTypes.func,
  onOpenFilter: PropTypes.func,
  onCloseFilter: PropTypes.func,
  formik: PropTypes.object
};

export default function ShopFilterSidebar({
                                            writeQ,
                                            writeT,
                                            isOpenFilter,
                                            onResetFilter,
                                            onOpenFilter,
                                            onCloseFilter,
                                            formik
                                          }) {
  const { values, getFieldProps, handleChange } = formik;

  return (
      <>
        <Button
            disableRipple
            color="inherit"
            endIcon={<Icon icon={roundFilterList} />}
            onClick={onOpenFilter}
        >
          Filters&nbsp;
        </Button>

        <FormikProvider value={formik}>
          <Form autoComplete="off" noValidate>
            <Drawer
                anchor="right"
                open={isOpenFilter}
                onClose={onCloseFilter}
                PaperProps={{
                  sx: { width: 280, border: 'none', overflow: 'hidden' }
                }}
            >
              <Stack
                  direction="row"
                  alignItems="center"
                  justifyContent="space-between"
                  sx={{ px: 1, py: 2 }}
              >
                <Typography variant="subtitle1" sx={{ ml: 1 }}>
                  Filters
                </Typography>
                <IconButton onClick={onCloseFilter}>
                  <Icon icon={closeFill} width={20} height={20} />
                </IconButton>
              </Stack>

              <Divider />

              <Scrollbar>
                <Stack spacing={3} sx={{ p: 3 }}>
                  {writeQ || writeT ?
                      <div>
                        <Typography variant="subtitle1" gutterBottom>
                          Author
                        </Typography>
                        <RadioGroup {...getFieldProps('author')}>
                          {FILTER_AUTHOR_OPTIONS.map((item) => (
                              <FormControlLabel
                                  key={item.value}
                                  value={item.value}
                                  control={<Radio />}
                                  label={item.label}
                              />
                          ))}
                        </RadioGroup>
                      </div> : null}
                  <div>
                    <Typography variant="subtitle1" gutterBottom>
                      Category
                    </Typography>
                    <RadioGroup {...getFieldProps('category')}>
                      {FILTER_CATEGORY_OPTIONS.map((item) => (
                          <FormControlLabel key={item} value={item} control={<Radio />} label={item} />
                      ))}
                    </RadioGroup>
                  </div>

                  <div>
                    <Typography variant="subtitle1" gutterBottom>
                      Zone
                    </Typography>
                    <RadioGroup {...getFieldProps('zone')}>
                      {FILTER_PRICE_OPTIONS.map((item) => (
                          <FormControlLabel
                              key={item.value}
                              value={item.value}
                              control={<Radio />}
                              label={item.label}
                          />
                      ))}
                    </RadioGroup>
                  </div>
                </Stack>
              </Scrollbar>

              <Box sx={{ p: 3 }}>
                <Button
                    fullWidth
                    size="large"
                    type="submit"
                    color="inherit"
                    variant="outlined"
                    onClick={onResetFilter}
                    startIcon={<Icon icon={roundClearAll} />}
                >
                  Clear All
                </Button>
              </Box>
            </Drawer>
          </Form>
        </FormikProvider>
      </>
  );
}

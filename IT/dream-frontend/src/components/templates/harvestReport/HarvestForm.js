import * as React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';

export default function HarvestForm() {

    const dateNow = ()=>{
        const t = new Date();
        const date = ('0' + t.getDate()).slice(-2);
        const month = ('0' + (t.getMonth() + 1)).slice(-2);
        const year = t.getFullYear();

        return `${date}/${month}/${year}`;
    }
    return (
        <React.Fragment>
            <Typography variant="h6" gutterBottom>
                Harvest
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                    <TextField
                        disabled
                        id="firstName"
                        name="firstName"
                        label="First name"
                        fullWidth
                        autoComplete="given-name"
                        variant="standard"
                        value={"Mark"}
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <TextField
                        disabled
                        id="lastName"
                        name="lastName"
                        label="Last name"
                        fullWidth
                        autoComplete="family-name"
                        variant="standard"
                        value={"Green"}
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <TextField
                        disabled
                        id="date"
                        name="date"
                        label="Date"
                        fullWidth
                        autoComplete="date"
                        variant="standard"
                        value={dateNow()}
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <TextField
                        disabled
                        id="zone"
                        name="zone"
                        label="Zone"
                        fullWidth
                        autoComplete="zone"
                        variant="standard"
                        value={"Good Zone"}
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        required
                        id="Corp name"
                        name="Corp name"
                        label="Corp name"
                        fullWidth
                        autoComplete="crop-name"
                        variant="standard"
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        required
                        id="Quantity kg"
                        name="Quantity kg"
                        label="Quantity kg"
                        fullWidth
                        autoComplete="Quantity-kg"
                        variant="standard"
                    />
                </Grid>
                <Grid item xs={12}>
                    <TextField
                        required
                        id="Crop category"
                        name="Crop category"
                        label="Crop category"
                        fullWidth
                        autoComplete="Crop-category"
                        variant="standard"
                    />
                </Grid>

                {/*
                <Grid item xs={12}>
                    <FormControlLabel
                        control={<Checkbox color="secondary" name="saveAddress" value="yes" />}
                        label="Use this address for payment details"
                    />
                </Grid>
                */}
            </Grid>
        </React.Fragment>
    );
}
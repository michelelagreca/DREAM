import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import axiosInstance from "../../axios";

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export default function SignUpFirst() {
    const [selectedRole, setSelectedRole] = useState({farmer: true, agronomist: false, policymaker:false})
    //Latitudes range from -90 to 90, and longitudes range from -180 to 80.
    const [position, setPosition] = useState({latitude: 200, longitude: 200})
    const navigation = useNavigate()
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        // eslint-disable-next-line no-console

        // acquire data from form
        const form_obj = {
            firstName: data.get('firstName'),
            lastName: data.get('lastName'),
            authcode: data.get("authcode"),
            email: data.get("email"),
            role: selectedRole.farmer ? 'farmer' : selectedRole.agronomist ? 'agronomist' : 'policymaker',
            password1: data.get("password"),
            password2: data.get("confirm-password"),
            latitude: position.latitude,
            longitude: position.longitude,
        };
         // soft validation
        if (form_obj.password1 !== form_obj.password2){
            alert('Password confirmation error')
            return
        }
        if (selectedRole.farmer && (form_obj.latitude === 200 || form_obj.longitude === 200)){
            alert('Sign up is not possible without access to your location')
            return
        }
        if (!form_obj.firstName || !form_obj.lastName || !form_obj.authcode || !form_obj.email || !form_obj.password1 || !form_obj.role ){
            alert('Missing mandatory field, complete the forum and try again')
            return
        }
        /*
        { example post
            "email":"c@c.it",
            "first_name":"Mark",
            "last_name":"doe",
            "auth_code":"AA",
            "password":"admin",
            "role":"agronomist",
            "user_name":"farmer1",
            "latitude":2,
            "longitude":3
        }*/

        const post_obj = {
            email:form_obj.email,
            first_name:capitalizeFirstLetter(form_obj.firstName),
            last_name:capitalizeFirstLetter(form_obj.lastName),
            auth_code:form_obj.authcode,
            password:form_obj.password1,
            role:form_obj.role,
            user_name:"" + form_obj.role + form_obj.email,
            latitude: form_obj.latitude,
            longitude: form_obj.longitude
        }
        //console.log(post_obj)
        axiosInstance
            .post(`user/register/`, post_obj)
            .then((res) =>{
                alert("You can now login")
                navigation('/login')
            })
            .catch((e)=>alert(e.response.status + " the inserted data is not valid for signing up"))
    };

    // get position of the user
    useEffect(()=>{
        navigator.geolocation.getCurrentPosition(function(position) {
            //console.log("Latitude is :", position.coords.latitude);
            //console.log("Longitude is :", position.coords.longitude);
            setPosition({latitude: position.coords.latitude, longitude: position.coords.longitude})
        });
    },[])
    const handleCheckbox = (role)=> {

        if (role === 'farmer') {
            setSelectedRole({farmer: true, agronomist: false, policymaker: false})
        } else if (role === 'agronomist') {
            setSelectedRole({farmer: false, agronomist: true, policymaker: false})
        } else if (role === 'policymaker') {
            setSelectedRole({farmer: false, agronomist: false, policymaker: true})
        }

    }

    return (

        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >

                <LockOutlinedIcon />

                <Typography component="h1" variant="h5">
                    Sign Up
                </Typography>
                <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                autoComplete="given-name"
                                name="firstName"
                                required
                                fullWidth
                                id="firstName"
                                label="First Name"
                                autoFocus
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="family-name"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <FormControlLabel
                                onClick={()=>handleCheckbox('policymaker')}
                                control={<Checkbox value="role" color="primary" checked={selectedRole.policymaker}/>}
                                label="Policy Maker"
                            />
                            <FormControlLabel
                                onClick={()=>handleCheckbox('agronomist')}
                                control={<Checkbox value="role" color="primary" checked={selectedRole.agronomist}/>}
                                label="Agronomist"
                            />
                            <FormControlLabel
                                onClick={()=>handleCheckbox('farmer')}
                                control={<Checkbox value="role" color="primary" checked={selectedRole.farmer}/>}
                                label="Farmer"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                id="authcode"
                                label="Authorization Code"
                                name="authcode"
                                autoComplete="authcode"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="new-password"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                name="confirm-password"
                                label="Confirm Password"
                                type="password"
                                id="confirm-password"
                                autoComplete="confirm-password"
                            />
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Sign Up
                    </Button>
                    {/*<Grid container justifyContent="flex-end">
                            <Grid item>
                                <Link href="#" variant="body2">
                                    Already have an account? Sign in
                                </Link>
                            </Grid>
                        </Grid>
                        */}
                </Box>
            </Box>
            {/*<Copyright sx={{ mt: 5 }} />*/}
        </Container>

    );
}
import React, {useEffect, useState} from 'react'
import LogoOnlyLayout from "../util/layouts/LogoOnlyLayout";
import DashboardLayout from "../util/layouts/DashboardLayout";
import axiosInstance from "../../axios";
import {useNavigate} from "react-router-dom";

//this component is displayed in the head of the page allowing to hide the sidebar
const Base = ({isLogoOnlyLayout = true, userTypeInit}) =>{
    // possibilities: anonymous, farmer, agronomist, policyMaker
    const[userType, setUserType] = useState(userTypeInit)
    const navigation = useNavigate()

    //automatically detect login
    useEffect(()=>{
        axiosInstance
            .get(`user/info/`,)
            .then((res) =>{
                if(res.data[0]) {
                    if (!res.data[0].role) {
                        setUserType('anonymous')
                    }
                    else if(res.data[0].role === 'agronomist') {
                        setUserType('agronomist')
                        navigation('/agronomist/forum')
                    }
                    else if(res.data[0].role === 'policymaker') {
                        setUserType('policyMaker')
                        navigation('/policymaker/forum')
                    }
                    else if(res.data[0].role === 'farmer') {
                        setUserType('farmer')
                        navigation('/farmer/forum')
                    }
                }
            })
            .catch((e)=>alert(e))
    },[])

    return(
        isLogoOnlyLayout ?
            <LogoOnlyLayout/>
            : <DashboardLayout userType={userType} setUserType={setUserType}/>
    )
}
export default Base
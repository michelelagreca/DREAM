import React, {useEffect, useState} from 'react'
import LogoOnlyLayout from "../util/layouts/LogoOnlyLayout";
import DashboardLayout from "../util/layouts/DashboardLayout";
import axiosInstance from "../../axios";

//this component is displayed in the head of the page allowing to hide the sidebar
const Base = ({isLogoOnlyLayout = true, userTypeInit}) =>{
    // possibilities: anonymous, farmer, agronomist, policyMaker
    const[userType, setUserType] = useState(userTypeInit)
    return(
        isLogoOnlyLayout ?
            <LogoOnlyLayout/>
            : <DashboardLayout userType={userType} setUserType={setUserType}/>
    )
}
export default Base
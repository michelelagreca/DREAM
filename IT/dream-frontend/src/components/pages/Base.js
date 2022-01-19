import React, {useEffect, useState} from 'react'
import LogoOnlyLayout from "../util/layouts/LogoOnlyLayout";
import DashboardLayout from "../util/layouts/DashboardLayout";

//this component is displayed in the head of the page allowing to hide the sidebar
const Base = ({isLogoOnlyLayout = true, userTypeInit}) =>{
    // possibilities: anonymous, farmer, agronomist, policyMaker
    //TODO add here mechanism to understand which user is logged id

    const [appState, setAppState] = useState({
        loading: false,
        posts: null,
    });

    useEffect(() => {
        setAppState({ loading: true });
        const apiUrl = `http://127.0.0.1:8000/api/1`;
        fetch(apiUrl)
            .then((data) => data.json())
            .then((posts) => {
                setAppState({ loading: false, posts: posts });
            });
    }, [setAppState]);

    const[userType, setUserType] = useState(userTypeInit)
    console.log(appState)
    return(
        isLogoOnlyLayout ?
            <LogoOnlyLayout/>
            : <DashboardLayout userType={userType} setUserType={setUserType}/>
    )
}
export default Base
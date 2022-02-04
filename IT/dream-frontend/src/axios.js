import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000/api/';

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,  // timeout in ms
    headers: {
        Authorization: localStorage.getItem('access_token')
            ? 'JWT ' + localStorage.getItem('access_token')
            : null,
        'Content-Type': 'application/json',
        accept: 'application/json',
    },
});

axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    async function (error) {            //handle token errors
        const originalRequest = error.config;

        console.log('@ERROR HANDLER')
        if (typeof error.response === 'undefined') {
            alert(
                'A server/network error occurred. ' +
                'Looks like CORS might be the problem. ' +
                'Sorry about this - we will get it fixed shortly.'
            );
            return Promise.reject(error);
        }


        console.log(error.response.status)
        console.log("original " + originalRequest.url)
        console.log("original->  " + error.response.data.code)

        if (
            error.response.data.code === 'token_not_valid' &&
            error.response.status === 401 &&
            error.response.statusText === 'Unauthorized' &&
            originalRequest.url === '/token/refresh/'
        ) {
            console.log('@FINAL REJECTION')
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            axiosInstance.defaults.headers['Authorization'] = null;
            alert("Login session invalid, please login again")
            window.location.href = '/login';
            return Promise.reject(error);
        }

        // handle token expiration and refresh
        if (
            error.response.data.code === 'token_not_valid' &&
            error.response.status === 401 &&
            error.response.statusText === 'Unauthorized'
        ) {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                //const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));
                console.log('@REFRESH TOKEN ')

                return axiosInstance
                    .post('/token/refresh/', { refresh: refreshToken })
                    .then((response) => {
                        console.log('@UPDATE ACCESS TOKEN')
                        localStorage.setItem('access_token', response.data.access);

                        axiosInstance.defaults.headers['Authorization'] =
                            'JWT ' + response.data.access;
                        originalRequest.headers['Authorization'] =
                            'JWT ' + response.data.access;
                        console.log('@REFRESHED SUCCESSFULLY ')
                        return axiosInstance(originalRequest);
                    })
                    .catch((err) => {
                        console.log('Refresh token failed.');
                        //window.location.href = '/login/';
                        console.log(err);
                    })
            }
            else {
                console.log('Refresh token not available.');
                return Promise.reject(error);
            }
        }

        console.log('Default handler');
        return Promise.reject(error);
    }
);

export default axiosInstance
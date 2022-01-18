import React, {useState} from 'react';
// routes
import Router from './routes';
// theme
import ThemeConfig from './theme';
import GlobalStyles from './theme/globalStyles';
// components
import ScrollToTop from './components/util/ScrollToTop';
//import { BaseOptionChartStyle } from './components/charts/BaseOptionChart';


// ----------------------------------------------------------------------

export default function App() {
    return (
        <ThemeConfig>
            <ScrollToTop />
            <GlobalStyles />
            {/*<BaseOptionChartStyle />*/}
            <Router />
        </ThemeConfig>
    );
}

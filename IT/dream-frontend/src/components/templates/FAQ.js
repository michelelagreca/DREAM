import PropTypes from 'prop-types';
import { formatDistance } from 'date-fns';
import {Box, Stack, Link, Card, Button, Divider, Typography, CardHeader, IconButton, Container} from '@mui/material';
import React, {useState} from "react";
import Page from "../util/Page";
import Logo from "../util/Logo";

export default function Faq() {
    return (
        <Page title="FAQ">
            <Container>
                <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
                    <Typography variant="h4" gutterBottom>
                        FAQ
                    </Typography>

                </Stack>
                <Logo/>
            </Container>
        </Page>
    );
}

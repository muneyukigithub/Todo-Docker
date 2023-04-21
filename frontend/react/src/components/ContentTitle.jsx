import { Box, Typography } from '@mui/material';
import React from 'react';
import styled from "styled-components";

export const ContentTitle = ({ title }) => {

    return (
        <TitleWrapper>
            <Title>{title}</Title>
        </TitleWrapper>
    )
}

const MainLayout = styled.div`
min-height: 100vh;
display: flex;
color:gray;
`;

const TitleWrapper = styled(Box)`
display: flex;
justify-content: center;
`

const Title = styled(Typography)`
font-size: 1.0rem;
width: 100%;
color: gray;
font-weight: lighter;
border-bottom: 0.5px solid black;
margin: 30px;
padding-bottom: 20px;
`
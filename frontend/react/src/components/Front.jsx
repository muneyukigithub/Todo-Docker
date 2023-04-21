import { Button } from '@mui/material';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import { fontSize } from '@mui/system';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from 'styled-components';

const linkStyle = {
    color: '#1976d2',
    fontWeight: 'bold',
    fontSize: "1rem"
};


export const Front = () => {
    return (
        <FrontWrapper>
            <FrontTitle>
                {"Todo管理画面"}
                {/* <FrontMainButton color='primary' variant='contained' size='large'> */}
                <Button>
                    <RouterLink to="/main" style={linkStyle} >
                        {"(Todoを作成する)"}
                    </RouterLink>
                </Button>

                {/* </FrontMainButton> */}
            </FrontTitle>
            <FrontImgWrapper>
                <img src='/images/TodoSample4.png' width={"100%"} height={"auto"} />
            </FrontImgWrapper>

            {/* <FrontMainLinkWrapper> */}


        </FrontWrapper>
    )
}

const FrontWrapper = styled.div`
display: flex;
flex-direction: column;
align-items: center;
margin-top: 100px;
/* font-family: 'Noto Sans', 'sans-serif','Courier New', Courier, monospace; */
`

const FrontTitle = styled(Typography)`
color: gray;
font-weight: bold;
font-size: xx-large;
`

const FrontImgWrapper = styled(Typography)`
display: flex;
justify-content: center;
width: 70%;
margin-bottom: 100px;
`

const FrontMainLinkWrapper = styled(Link)`
border-radius: 32px;
border: 2px solid ;
background-color: #1976d2;
/* position: fixed;
right:10px; */
/* &:hover{
    background: "#1976d294"
}; */
`

const FrontMainLink = styled(RouterLink)`
font-size: x-large;
text-decoration: none;
padding: 0 10px;
font-weight: bold;
color: "#FFF"
`

const FrontMainButton = styled(Button)`
/* margin: 30px; */

`

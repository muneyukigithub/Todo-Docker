import { Button } from '@mui/material';
import Typography from '@mui/material/Typography';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from 'styled-components';
import sampleImg from '../../public/images/todosample4.png';

const linkStyle = {
    color: '#1976d2',
    fontWeight: 'bold',
    fontSize: '1rem',
};

export const Front = () => {
    return (
        <FrontWrapper>
            <FrontTitle>
                {'Todo管理画面'}
                <Button>
                    <RouterLink to="/main" style={linkStyle}>
                        {'Todoを作成する'}
                    </RouterLink>
                </Button>
            </FrontTitle>
            <FrontImgWrapper>
                <img src={sampleImg} width={'100%'} height={'auto'} />
            </FrontImgWrapper>
        </FrontWrapper>
    );
};

const FrontWrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 100px;
    /* font-family: 'Noto Sans', 'sans-serif','Courier New', Courier, monospace; */
`;

const FrontTitle = styled(Typography)`
    color: gray;
    font-weight: bold;
    font-size: xx-large;
`;

const FrontImgWrapper = styled(Typography)`
    display: flex;
    justify-content: center;
    width: 70%;
    margin-bottom: 100px;
`;

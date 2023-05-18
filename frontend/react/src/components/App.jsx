import { CssBaseline } from '@mui/material';
import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Front } from './Front';
import { Header } from './Header';
import { LogoutComplete } from './LogoutComplete';
import { MainLayout } from './MainLayout';
import NotFound from './NotFound';
import RegistComplete from './RegistComplete';
import Register from './Register';
import SignIn from './Signin';
import { UserProvider } from './UserContext';
import { TaskListProvider } from './TaskListContext';
import UserDeactivateComplete from './UserDeactivateComplete';
import { UserDeleteComplete } from './UserDeleteComplete';

const App = () => {
    const drawerWidth = 400;
    const headerHeight = 64;

    return (
        <BrowserRouter>
            <CssBaseline />
            <TaskListProvider>
                <UserProvider>
                    <Header headerHeight={headerHeight} />

                    <Routes>
                        {/* フロント画面 */}
                        {/* <Route path="/" element={<Front />} /> */}
                        {/* メイン画面 */}
                        <Route
                            path="/"
                            element={<MainLayout headerHeight={headerHeight} drawerWidth={drawerWidth} />}
                        />

                        {/* ログイン画面 */}
                        <Route path="/login" element={<SignIn />} />

                        {/* ログアウト完了画面 */}
                        <Route path="/logoutcomplete" element={<LogoutComplete />} />

                        {/* ユーザー登録画面 */}
                        <Route path="/regist" element={<Register />} />

                        {/* ユーザー登録完了画面 */}
                        <Route path="/registcomplete" element={<RegistComplete />} />

                        {/* ユーザー削除完了画面 */}
                        <Route path="/userdeletecomplete" element={<UserDeleteComplete />} />

                        {/* ユーザー退会完了画面 */}
                        <Route path="/UserDeactivateComplete" element={<UserDeactivateComplete />} />

                        {/* メイン画面
                        <Route
                            path="/main"
                            element={<MainLayout headerHeight={headerHeight} drawerWidth={drawerWidth} />}
                        /> */}

                        <Route path="*" element={<NotFound />} />
                    </Routes>
                </UserProvider>
            </TaskListProvider>
        </BrowserRouter>
    );
};

export default App;

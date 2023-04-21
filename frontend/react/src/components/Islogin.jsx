import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios, { authAxios } from './defaultaxios';
import { useUser } from "./UserContext";

const refresh = async () => {
    return axios.get("/jwt_refresh/")
}

const useAuthAxios = () => {
    authAxios.interceptors.response.use(
        (response) => response,
        async (error) => {
            const prevRequest = error?.config;
            if (error.response.status === 401 && !prevRequest.sent) {
                prevRequest.sent = true;
                try {
                    await refresh()
                    return authAxios(prevRequest)
                } catch {
                    return Promise.reject(error);
                }
            }
            return Promise.reject(error);
        }
    )


    return authAxios;
}

export const Islogin = ({ AuthSuccessComponent, AuthFaildComponent }) => {
    const authAxios = useAuthAxios();

    // メモ：hooksを呼び出す前にreturnするとエラーになる
    // 条件付きでuseXxxを呼び出す、useXxxが呼ばれる前にreturnする等もダメ

    const navigate = useNavigate();
    const UserContext = useUser();
    const [loading, setLoading] = useState(true);
    const [verify, setVerify] = useState(false);

    useEffect(() => {
        const loginDault = async () => {
            try {
                await authAxios.get("/jwt_verifyaccesstoken/");
                console.log("ok");
                setVerify(true);
            } catch (error) {
                console.log("error");
                setVerify(false);
            } finally {
                setLoading(false);
            }
        };

        loginDault()
    }, [AuthSuccessComponent])


    if (loading) return <p>...loading</p>
    if (!verify || !UserContext.user) {
        navigate("/login")
    }

    return AuthSuccessComponent
};
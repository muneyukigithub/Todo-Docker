import axios from 'axios';
import dotenv from 'dotenv';
// dotenv.config();
// require('dotenv').config();
const BASE_URL = process.env.REACT_APP_API_URL

export default axios.create({
    baseURL: BASE_URL,
    withCredentials: true
});


export const authAxios = axios.create({
    baseURL: BASE_URL,
    headers: { "Content-Type": "application/json" },
    withCredentials: true
})
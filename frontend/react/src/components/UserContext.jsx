import React, { useEffect } from 'react';
import { useState } from 'react';
import { useContext } from 'react';

const UserContext = React.createContext(null);

export const useUser = () => {
    return useContext(UserContext);
};

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const userinfojson = localStorage.getItem('userinfo');

    useEffect(() => {
        if (userinfojson) {
            const userinfo = JSON.parse(userinfojson);
            setUser(userinfo);
        }
    }, [userinfojson]);

    const handlelogout = () => {
        setUser(null);

        localStorage.removeItem('userinfo');
    };

    const value = {
        user: user,
        setUser: setUser,
        logout: handlelogout,
    };

    return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};

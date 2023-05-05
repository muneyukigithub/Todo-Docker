import { Link } from 'react-router-dom';
import React from 'react';

const NotFound = () => {
    return (
        <>
            <h1>お探しのページが見つかりませんでした。</h1>
            <div>
                <Link to={`/`}>ホームに戻る</Link>
            </div>
        </>
    );
};

export default NotFound;

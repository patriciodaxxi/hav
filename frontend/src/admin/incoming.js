import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Uploader from './Uploader'
import Admin from './Admin'


ReactDOM.render(
    <App>
        <Admin>
            <Uploader />
        </Admin>
    </App>,
    document.getElementById('root')
);
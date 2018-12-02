import './index.css';
import React from 'react';
import ReactDOM from 'react-dom';
import Main from './main';
import reducer from "./services/reduxStorage/reducer";
import {createStore} from 'redux';
import {Provider} from 'react-redux';

import registerServiceWorker from './registerServiceWorker';


const store = createStore(reducer);

ReactDOM.render(
    <Provider store={store}>
        <Main/>
    </Provider>,
    document.getElementById('root')
);

registerServiceWorker();

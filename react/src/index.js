import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import PledgeApp from './pledgeApp';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<PledgeApp />, document.getElementById('root'));
registerServiceWorker();

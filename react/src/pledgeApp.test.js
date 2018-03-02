import React from 'react';
import ReactDOM from 'react-dom';
import PledgeApp from './pledgeApp';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<PledgeApp />, div);
  ReactDOM.unmountComponentAtNode(div);
});

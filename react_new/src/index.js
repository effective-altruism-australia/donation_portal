import "./index.css";
import React from "react";
import ReactDOM from "react-dom/client";
import reducer from "./services/reduxStorage/reducer";
import { legacy_createStore as createStore } from "redux";
import { Provider } from "react-redux";
import App from "./App";

const store = createStore(reducer);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);

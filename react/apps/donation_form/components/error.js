import React from "react";

export default function Error(props) {
    return props.visible ? <div className="error-text">{props.children}</div> : null;
}
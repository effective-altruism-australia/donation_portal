import React from "react";

export const customInput = (props) => {
    let {input, type, meta} = props;
    return (<div>
        <input {...input} {...props} type={type} />
        {meta.touched &&
        ((meta.error && <div className="text-danger">{meta.error}</div>) ||
            (meta.warning && <div className="text-warning">{meta.warning}</div>))}
    </div>);
};

export const customCurrencyInput = (props) => {
    let {input, type, meta} = props;
    return (
        <div>
            <div className="input-group amount-input">
                <span className="input-group-addon">$</span>
                <input {...input} {...props} type={type} />
            </div>
            {meta.touched &&
            ((meta.error && <div className="text-danger">{meta.error}</div>) ||
                (meta.warning && <div className="text-warning">{meta.warning}</div>))}
        </div>
   );
};

export const cardNumberInput = (props) => {
    let {input, type, meta} = props;
    return (
        <div>
            <div className="input-group">
                <input className={props.className} {...input} {...props} type={type} />
                <span className="input-group-addon"><span className="glyphicon glyphicon-lock"/></span>
            </div>
            {meta.touched &&
            ((meta.error && <div className="text-danger">{meta.error}</div>) ||
                (meta.warning && <div className="text-warning">{meta.warning}</div>))}
        </div>
    );
};


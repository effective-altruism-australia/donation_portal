// Original code is from:
// https://github.com/chenglou/react-radio-group/blob/master/index.jsx. The
// package appears to be unmaintained and was using a Legacy context API which is
// throwing errors. I've refactored the code to use the new context API here.
// -- Nathan Sherburn 2023

import PropTypes from 'prop-types';
import React, { createContext } from 'react';

const RadioContext = createContext();

export const Radio = (props) => {
  return (
    <RadioContext.Consumer>
      {(context) => {
        const { name, selectedValue, onChange } = context.radioGroup;
        const optional = {};

        if (selectedValue !== undefined) {
          optional.checked = (props.value === selectedValue);
        }

        if (typeof onChange === 'function') {
          optional.onChange = () => onChange(props.value);
        }

        return (
          <input
            {...props}
            aria-checked={optional.checked}
            type="radio"
            name={name}
            {...optional}
          />
        );
      }}
    </RadioContext.Consumer>
  );
};

Radio.propTypes = {
  value: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
    PropTypes.bool,
  ]).isRequired,
};

export class RadioGroup extends React.Component {
  render() {
    const { Component, name, selectedValue, onChange, children, ...rest } = this.props;
    const radioGroupContext = {
      radioGroup: {
        name,
        selectedValue,
        onChange,
      },
    };

    return (
      <RadioContext.Provider value={radioGroupContext}>
        <Component role="radiogroup" {...rest}>
          {children}
        </Component>
      </RadioContext.Provider>
    );
  }
}

RadioGroup.defaultProps = {
  Component: "div",
};

RadioGroup.propTypes = {
  name: PropTypes.string,
  selectedValue: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
    PropTypes.bool,
  ]),
  onChange: PropTypes.func,
  children: PropTypes.node.isRequired,
  Component: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.func,
    PropTypes.object,
  ]),
};

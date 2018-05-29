import {
    SET_CHARITY,
    SET_DONATION_RESULT
} from "./actionTypes";
import { reducer as formReducer } from 'redux-form'

import {combineReducers} from 'redux';

let charityState = {
    currentCharity: null
};

function charityReducer(state = charityState, action) {
    switch(action.type) {
        case SET_CHARITY:
            return Object.assign({}, state, {
                currentCharity: action.value
            });
        default:
            return state;
    }
}
function resultReducer(state = {}, action) {
    switch(action.type) {
        case SET_DONATION_RESULT:
            return Object.assign({}, state, action.value);
        default:
            return state;
    }
}

export default combineReducers({
    charity: charityReducer,
    form: formReducer,
    result: resultReducer

})

import {
    SET_CHARITY,
    SET_DONATION_RESULT
} from "./actionTypes";

export function setCharity(value) {
    return {
        type: SET_CHARITY,
        value: value
    };
}

export function setDonationResult(result) {
    return {
        type: SET_DONATION_RESULT,
        value: result
    }
}

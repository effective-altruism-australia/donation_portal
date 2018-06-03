function safeInteger(val) {
    let intval = parseInt(val);
    return isNaN(intval) ? 0 : intval;
}

export function getTotalDonation(mode, amount, contribute) {
    let total = 0;
    console.log(amount);
    if (mode === 'auto') {
        if (amount) {
            if (amount.preset !== "other") {
                total += safeInteger(amount.preset);
            } else if (amount.value) {
                total += safeInteger(amount.value);
            }
        }
    } else if (mode === 'custom') {
        for (let prop in amount) {
            if (prop !== "preset") {
                total += safeInteger(amount[prop]);
            }
        }
    }


    if (contribute && contribute.value) {
        total += safeInteger(contribute.value);
    }

    return total;
}

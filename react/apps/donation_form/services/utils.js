function safeFloat(val) {
    let floatval = parseFloat(val);
    return isNaN(floatval) ? 0 : floatval;
}

export function getTotalDonation(mode, amount, contribute) {
    let total = 0;
    if (mode === 'auto') {
        if (amount) {
            if (amount.preset !== "other") {
                total += safeFloat(amount.preset);
            } else if (amount.value) {
                total += safeFloat(amount.value);
            }
        }
    } else if (mode === 'custom') {
        for (let prop in amount) {
            if (prop !== "preset" && prop !== "value") {
                total += safeFloat(amount[prop]);
            }
        }
    }


    if (contribute && contribute.value) {
        total += safeFloat(contribute.value);
    }

    return total;
}

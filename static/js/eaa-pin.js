!function() {
"use strict";
function t(t) {
window.console && (console.warn ? console.warn(t) :console.log && console.log(t));
}
var e, n = "https://api.pin.net.au";
"https:" != window.location.protocol && t("It is recommended that you host your payment page using SSL (HTTPS)");
var i = function() {
function t() {
return i + ++r;
}
function n(t, e, n) {
var i = t.replace(/\?$/, n);
for (var r in e) i += "&", i += encodeURIComponent(r), i += "=", i += encodeURIComponent(e[r]);
return i += "&" + new Date().getTime();
}
var i = "PinJsCallback", r = 0;
return function(i, r, o) {
var s = t(), a = document.createElement("script");
a.src = n(i, r, s), a.async = !0, window[s] = function() {
try {
delete window[s];
} catch (t) {
window[s] = e;
}
a.parentElement.removeChild(a), o.apply(window, arguments);
}, (document.head || document.getElementsByTagName("head")[0]).appendChild(a);
};
}(), r = null;
window.Pin || (window.Pin = {}), Pin.setPublishableKey = function(t) {
r = t;
}, Pin.createToken = function(t, e) {
if (!r) throw new Error("Pin.publishable_api_key has not been set");
t.publishable_api_key = r, t._method = "POST", i(n + "/1/cards.json?callback=?", t, e);
};
}();
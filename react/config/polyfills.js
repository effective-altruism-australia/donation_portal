if (typeof Promise === 'undefined') {
    // Rejection tracking prevents a common issue where React gets into an
    // inconsistent state due to an error, but it gets swallowed by a Promise,
    // and the user has no idea what causes React's erratic future behavior.
    require('promise/lib/rejection-tracking').enable();
    window.Promise = require('promise/lib/es6-extensions.js');
}

// fetch() polyfill for making API calls.
require('whatwg-fetch');

// Object.assign() is commonly used with React.
// It will use the native implementation if it's present and isn't buggy.
Object.assign = require('object-assign');


// Note: From this point on, we're getting into our own additions.
//       I'm adding things as I notice they're required. ~ James

// Array.from
// if (!Array.from) Array.from = require('array-from');

// Symbol
// if (typeof Symbol === 'undefined') {
//     window.Symbol = require('es6-symbol');
// }
//
// // Various iterators
// require('iterators-polyfill');
//
// // String.trimLeft(), String.trimRight()
// var trimLeft = require('string.prototype.trimleft');
// if (!String.prototype.trimLeft) {
//     trimLeft.shim();
// }
// var trimRight = require('string.prototype.trimright');
// if (!String.prototype.trimRight) {
//     trimRight.shim();
// }
//
// Array.prototype.findIndex = Array.prototype.findIndex || function (callback) {
//     if (this === null) {
//         throw new TypeError('Array.prototype.findIndex called on null or undefined');
//     } else if (typeof callback !== 'function') {
//         throw new TypeError('callback must be a function');
//     }
//     var list = Object(this);
//     // Makes sures is always has an positive integer as length.
//     var length = list.length >>> 0;
//     var thisArg = arguments[1];
//     for (var i = 0; i < length; i++) {
//         if (callback.call(thisArg, list[i], i, list)) {
//             return i;
//         }
//     }
//     return -1;
// };

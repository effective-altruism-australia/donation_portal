// 'apps' exports a mapping from app names to module paths.
// To add another app, give it an entry below, with the name to use from Django, and then its source directory.

module.exports.apps = {
    'donation_form': 'donation_form',
};

// Additionally, we export the name of the app to use when running webpack dev server.
// module.exports.devServerAppName = 'api-documentation';
//
//
// if (module.exports.apps[module.exports.devServerAppName] == null) {
//     if (process.env.NODE_ENV !== 'development') {
//         console.warn(`'devServerAppName' (${module.exports.devServerAppName}) doesn't exist in our set of apps. Please correct it.`);
//     } else {
//         console.error(`'devServerAppName' (${module.exports.devServerAppName}) doesn't exist in our set of apps. Aborting.`);
//         process.exit(1);
//     }
// }

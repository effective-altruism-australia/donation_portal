const path = require('path');
const autoprefixer = require('autoprefixer');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const findCacheDir = require('find-cache-dir');
const CaseSensitivePathsPlugin = require('case-sensitive-paths-webpack-plugin');
const WebpackCleanupPlugin = require('webpack-cleanup-plugin');
const getClientEnvironment = require('./env');
const _ = require('underscore');

// 'apps' exports a dictionary mapping app names to relative module paths.
const apps = require('../apps').apps;
const appsDirectory = path.dirname(require.resolve('../apps'));

// Get environment variables to inject into our app.
const env = getClientEnvironment();


// This is the configuration for building bundles for Django in development.
// It's focused on developer experience and fast rebuilds.

module.exports = {
    // This makes the bundle appear split into separate modules in the devtools.
    devtool: 'eval',

    // This builds an entry point for each app, named by their names in `apps/index.js`.
    entry: _.mapObject(apps, appSubmodulePath => [
        // Some polyfills.
        require.resolve('./polyfills'),
        // The app code.
        require.resolve(`../apps/${appSubmodulePath}`),
    ]),

    output: {
        // The directory to place the built assets in.
        path: path.resolve(__dirname, '../build/bundle'),
        // The root from which content is served.
        publicPath: '/static/bundle/',
        // This is the JS bundle containing code for a particular app.
        filename: '[name].[chunkhash:8].js',
        // Add /* filename */ comments alongside imports.
        pathinfo: true,
    },

    resolve: {
        // Allow importing .json and .jsx, as well as .js and directories.
        extensions: ['.js', '.json', '.jsx', ''],
        alias: {
            // Support React Native Web by replacing all the relevant imports.
            'react-native': 'react-native-web'
        }
    },

    module: {
        // First, run the linter, before Babel processes the JS.
        preLoaders: [
            {
                test: /\.(js|jsx)$/,
                loader: 'eslint',
                include: appsDirectory,
            }
        ],
        loaders: [
            // JS is processed with Babel.
            {
                test: /\.(js|jsx)$/,
                include: appsDirectory,
                loader: 'babel',
                query: {
                    // This is a feature of `babel-loader` that enables caching results for faster rebuilds.
                    cacheDirectory: findCacheDir({name: 'babel-cache'})
                }
            },

            // "postcss" autoprefixes our CSS, "css" resolves paths and adds css assets as dependencies, and "style" turns CSS into JS modules that inject <style> tags.
            // In production, we use a plugin to extract that CSS to a file, but in development the "style" loader enables hot editing of CSS.
            {
                test: /\.css$/,
                loader: 'style!css?importLoaders=1!postcss'
            },

            // JSON is not enabled by default in Webpack.
            {
                test: /\.json$/,
                loader: 'json'
            },

            // "file" loader makes sure assets end up in static media.
            {
                test: /\.(ico|jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2)(\?.*)?$/,
                loader: 'file',
                query: {
                    name: 'static/react/media/[name].[hash:8].[ext]'
                }
            },

            // "url" loader works just like "file" loader but it also embeds small assets as data URLs to avoid requests.
            {
                test: /\.(mp4|webm|wav|mp3|m4a|aac|oga)(\?.*)?$/,
                loader: 'url',
                query: {
                    limit: 10000,
                    name: 'static/react/media/[name].[hash:8].[ext]'
                }
            }
        ]
    },

    // We use PostCSS for autoprefixing only.
    postcss: () => [
        autoprefixer({browsers: [
             '>1%',
             'last 4 versions',
             'Firefox ESR',
             'not ie < 9', // React doesn't support IE8 anyway
        ]}),
    ],

    plugins: [
        // This keeps track of Webpack builds for Django's usage.
        new BundleTracker({path: path.resolve(__dirname, '../build'), filename: 'webpack-stats.json',
                    logTime: true}),

        // This makes environment variables from `./env.js` available to the JS code, for example:
        // `if (process.env.NODE_ENV === 'development') { ... }`
        new webpack.DefinePlugin(env),

        // Watcher doesn't work well if you mistype casing in a path so we use a plugin that prints an error when you attempt to do this.
        new CaseSensitivePathsPlugin(),

        // This cleans up old bundles in the output directory.
        // ('quiet' suppresses its command line output.)
        new WebpackCleanupPlugin({quiet: true}),
    ],

    node: {
        // Some libraries import Node modules but don't use them in the browser. This tells Webpack to provide empty mocks for them so importing them works.
        fs: 'empty',
        net: 'empty',
        tls: 'empty',

        // This, in combination with context = __dirname, allows __filename to work in our source code.
        __filename: true,
    },

    // This allows __filename to work in our source code.
    context: __dirname,
};

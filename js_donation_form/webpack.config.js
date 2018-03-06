const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'public')
  },
  module: {
    rules: [
      { test: /\.html$/, use: 'ractive' },
      { test:/\.css$/, use:['style-loader','css-loader'] }
    ]
  },
  plugins: [
    new CopyWebpackPlugin([{ from: 'src/thumbnails', to: 'thumbnails' }])
  ]
};


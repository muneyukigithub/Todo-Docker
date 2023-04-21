const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require("html-webpack-plugin");
const webpack = require('webpack');

// index.htmlにscriptタグを追加してくれるプラグイン
const htmlPlugin = new HtmlWebpackPlugin({
  template: path.join(__dirname, "public", "index.html"),
  // filename: "index.html",
})

// const DefinePlugin = new webpack.DefinePlugin({
//   'process.env.REACT_APP_API_URL': JSON.stringify(process.env.REACT_APP_API_URL)
// })
const Dotenv = require('dotenv-webpack');

module.exports = {
  performance: {
    maxEntrypointSize: 700000,
    maxAssetSize: 700000,
  },
  entry: "./src/components/index.jsx", //ビルドするファイル
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        //js,jsxファイルのローダー設定
        test: /\.(js|jsx)$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      // ts,tsxファイルのローダー設定
      // {
      //   test: /\.tsx$/,         // 拡張子 .ts のファイルを
      //   use: 'ts-loader',         // ts-loaderでトランスパイルする
      //   exclude: /node_modules/,  // ただし外部ライブラリは除く
      // },
      {
        test: /\.(jpg|png)$/,
        loader: 'url-loader'
      }
    ],
  },
  resolve: {
    fallback: {
      "fs": false,
      "path": false,
      "os": false
    },
    modules: [path.resolve(__dirname, 'src'), path.resolve(__dirname, 'node_modules')],
    extensions: [
      '.jsx', '.js',
    ]
  },
  mode: 'development',
  //   module: {
  //   loaders: [
  //           //loader
  //     ]
  // }
  devServer: {
    // webpack-dev-serverの公開フォルダ
    // contentBase: __dirname + '/dist',
    open: true,//ブラウザ立ち上げを自動化
    hot: true,//ホットリロードon
    static: {
      directory: __dirname + '/public',//htmlやcssを配置したディレクトリをルートディレクトリとして指定
    },

    host: 'localhost',
    https: {
      key: fs.readFileSync('./localhost-key.pem'),
      cert: fs.readFileSync('./localhost.pem'),
    },
  },
  plugins: [
    // new HtmlWebpackPlugin()
    htmlPlugin,
    new Dotenv(),
    // new webpack.DefinePlugin({
    //   'process.env.REACT_APP_API_URL': JSON.stringify(process.env.REACT_APP_API_URL)
    // }),
  ],
};
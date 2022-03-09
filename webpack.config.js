const path = require('path');
const HtmlPlugin = require('html-webpack-plugin');

module.exports = {
    entry: "./src/main.ts",
    mode: "development",
    output: {
        filename: "./bundle.js"
    },
    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",
    resolve: {
        // Add '.ts' as resolvable extensions.
        extensions: [".ts", ".js"]
    },

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                loader: "ts-loader",
                options: {
                    appendTsSuffixTo: [/\.vue$/]
                }
            },
            {
                test: /\.vue$/,
                loader: "vue-loader"
            }
        ]
    },

    devServer: {
        static: path.join(__dirname, "./dist/"),
        compress: true,
        port: 8088
    },
    // Omit "externals" if you don't have any. Just an example because it's
    // common to have them.
    externals: {
        // Don't bundle giant dependencies, instead assume they're available in
        // the html doc as global variables node module name -> JS global
        // through which it is available
       //"pixi.js": "PIXI"
    },

    plugins:[
        new HtmlPlugin({
            template: path.join(__dirname, "src", "index.html"),
            filename: "index.html"
        })
    ]
};
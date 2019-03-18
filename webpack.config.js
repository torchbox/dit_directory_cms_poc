const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const sass = require('sass');

// Some libraries import Node modules but don't use them in the browser.
// Tell Webpack to provide empty mocks for them so importing them works.
const node = {
    dgram: 'empty',
    fs: 'empty',
    net: 'empty',
    tls: 'empty',
    child_process: 'empty',
};

const stats = {
    // Add chunk information (setting this to `false` allows for a less verbose output)
    chunks: false,
    // Add the hash of the compilation
    hash: false,
    // `webpack --colors` equivalent
    colors: true,
    // Add information about the reasons why modules are included
    reasons: false,
    // Add webpack version information
    version: false,
};

/**
 * Base Webpack config, defining how our code should compile.
 */
const webpackConfig = (environment) => {
    const isProduction = environment === 'production';

    const outputPath = path.join(
        __dirname,
        'richtext_poc',
        'static',
        'richtext_poc',
    );

    const compiler = {
        // Disable Webpack mode to use our own optimisations.
        mode: 'none',

        // See http://webpack.github.io/docs/configuration.html#devtool
        devtool: 'source-map',

        entry: {
            richtext_poc: ['./richtext_poc/static_src/richtext_poc.entry.js'],
        },
        output: {
            path: outputPath,
            filename: '[name].bundle.js',
        },
        plugins: [
            new webpack.NoEmitOnErrorsPlugin(),
            new BundleAnalyzerPlugin({
                // Can be `server`, `static` or `disabled`.
                analyzerMode: 'static',
                // Path to bundle report file that will be generated in `static` mode.
                reportFilename: path.join(__dirname, 'webpack-stats.html'),
                // Automatically open report in default browser
                openAnalyzer: false,
                logLevel: environment === 'production' ? 'info' : 'warn',
            }),

            new MiniCssExtractPlugin({
                filename: '[name].bundle.css',
            }),

            new webpack.HotModuleReplacementPlugin(),

            new webpack.DefinePlugin({
                'process.env.NODE_ENV': JSON.stringify(environment),
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.js$/,
                    use: ['babel-loader'],
                    exclude: /node_modules/,
                },

                {
                    test: /\.(scss|css)$/,
                    use: [
                        isProduction
                            ? MiniCssExtractPlugin.loader
                            : 'style-loader',
                        {
                            loader: 'css-loader',
                            options: {
                                sourceMap: !isProduction,
                            },
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                sourceMap: !isProduction,
                                plugins: () => [autoprefixer()],
                            },
                        },
                        {
                            loader: 'sass-loader',
                            options: {
                                sourceMap: !isProduction,
                                implementation: sass,
                            },
                        },
                    ],
                },
            ],
        },

        optimization: {
            minimize: isProduction,
            minimizer: [
                new UglifyJsPlugin({
                    sourceMap: true,

                    uglifyOptions: {
                        compress: {
                            warnings: false,
                            // Disabled because of an issue with Uglify breaking seemingly valid code:
                            // https://github.com/facebookincubator/create-react-app/issues/2376
                            // Pending further investigation:
                            // https://github.com/mishoo/UglifyJS2/issues/2011
                            comparisons: false,
                        },
                        output: {
                            comments: false,
                            // Turned on because emoji and regex is not minified properly using default
                            // https://github.com/facebookincubator/create-react-app/issues/2488
                            ascii_only: true,
                        },
                    },
                }),
            ],
            splitChunks: {
                cacheGroups: {
                    vendor: {
                        name: 'vendor',
                        chunks: 'initial',
                        minChunks: 2,
                        reuseExistingChunk: true,
                    },
                },
            },
        },

        // Turn off performance hints during development because we don't do any
        // splitting or minification in interest of speed. These warnings become
        // cumbersome.
        performance: {
            hints: isProduction && 'warning',
        },

        stats,

        node,
    };

    return compiler;
};

module.exports = webpackConfig;

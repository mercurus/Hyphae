const { defineConfig } = require("@vue/cli-service");
const BundleTracker = require("webpack-bundle-tracker");

// https://cli.vuejs.org/config/#pages
const pages = {
    main: "./src/main.ts",
}

module.exports = defineConfig({
    // publicPath: process.env.NODE_ENV === "production" ? "/static/vue" : "http://localhost:8080/",
    publicPath: "http://localhost:8080/",
    // publicPath: "/static/vue",
    outputDir: "../static/vue/",
    pages: pages,
    transpileDependencies: true,
    filenameHashing: false,
    productionSourceMap: false,
    css: {
        extract: true,
    },

    devServer: {
        port: 8080,
        host: "localhost",
        https: false,
        headers: { "Access-Control-Allow-Origin": ["*"] },
        hot: "only",
        devMiddleware: {
            // see https://github.com/webpack/webpack-dev-server/issues/2958
            writeToDisk: false, 
        },
        static: {
            watch: true
        }
    },

    chainWebpack: config => {
        config.optimization
        .splitChunks({
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: "chunk-common",
                    chunks: "all",
                    priority: 1
                },
            },
        });

        // delete HTML related webpack plugins
        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        });

        config.plugin("BundleTracker")
        .use(BundleTracker, [{
            path: "../vue_frontend/",
            filename: "webpack-stats.json",
        }]);
    }
});

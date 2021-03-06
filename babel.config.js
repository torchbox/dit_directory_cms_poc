module.exports = {
  presets: [
    [
      "@babel/preset-env",
      {
        modules: false,
      },
    ],
    "@babel/preset-react",
    "@babel/preset-flow",
  ],
  env: {
    test: {
      presets: [
        "@babel/preset-env",
        "@babel/preset-react",
        "@babel/preset-flow",
      ],
    },
  },
};

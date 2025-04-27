const path = require('path');

module.exports = {
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src/'),  // Resolve '@' to 'src' folder
    },
    extensions: ['.js', '.jsx', '.json'],
  },
};

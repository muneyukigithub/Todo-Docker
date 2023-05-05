module.exports = {
    "root": true,
    "env": {
        "node":true,
        "browser": true,
        "es2021": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:react/recommended"
    ],
    "overrides": [
    ],
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "plugins": [
        "react"
    ],
    "rules": {
        "no-console": "error",
        "react/prop-types": "off",
        "semi": ["error", "always"]
    }
}

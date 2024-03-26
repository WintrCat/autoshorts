# Autoshorts

### 📜 NPM Scripts
`npm run setup` Installs required Python and NPM packages.
<br>
`npm run build` Compiles TypeScript.
<br>
`npm start` Compiles TypeScript and runs entry point.

### 🔑 Environment Variables
`NODE_ENV` The environment in which the application is running; "dev" or "prod".
Used assets are not deleted when in the development environment.

### 📂 Asset feeding
Some of the video types require manually picked assets to produce
videos. For example, the Chess shorts require PGNs with brilliant
moves in them at hand. These assets should be placed in the `assets`
folder which should live in the root directory of the project. For
those hosting locally, you may have to create this folder yourself.
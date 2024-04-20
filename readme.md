# Autoshorts

### 🚀 Running Locally
#### Prerequisites
- Reasonably updated Node.js runtime installed
- TypeScript package installed
- Python 3.11 or later installed
- ImageMagick installed

#### Instructions
- `git clone` this repository or download as ZIP and extract it somewhere.
- `cd` into the root directory of the project in a terminal.
- `npm run setup` to install the required Python and Node.js packages.
- `npm start` to start the webserver for the interface.
- Go to `localhost:8080` on your browser unless you have defined another port.
- Generated shorts are stored in the `out` directory, which you will find in the project folder.

### 📜 NPM Scripts
`npm run setup` Installs required Python and NPM packages.
<br>
`npm run build` Compiles TypeScript for web interface.
<br>
`npm start` Compiles TypeScript and starts web interface on localhost.

### 🔑 Environment Variables
`PORT` The port that the webserver running the interface listens on. Defaults to 8080.

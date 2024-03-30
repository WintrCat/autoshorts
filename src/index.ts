import express from "express";
import path from "path";
import dotenv from "dotenv";
dotenv.config();

import { createSocketServer } from "./socket";

const app = express();

app.use("/", express.static("public"));

app.get("/", async (req, res) => {
    res.sendFile(path.resolve("public/index.html"));
});

const port = process.env.PORT || 8080;
const httpServer = app.listen(port, () => {
    console.log(`server running on port ${port}`);
});

createSocketServer(httpServer);
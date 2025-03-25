import express from "express";
import multer from "multer";
import { connectDB } from "./config/db.js";
import mongoose from "mongoose";
import cors from "cors";
import { spawn } from "child_process";
// import {path} from "path";
import 'dotenv/config'
import jobRouter from "./routes/jobRouter.js";
import resumeRouter from "./routes/resumeRouter.js";

const app = express();
const PORT = process.env.PORT || 4000;

// middleware
app.use(cors());
app.use(express.json()); //  handle json data
app.use(express.urlencoded({extended : false}));

connectDB();

// Serve Frontend (after build)
// app.use(express.static(path.join(__dirname, "../frontend/build")));

app.use('/api/jobs',jobRouter);
app.use('/api/resume',resumeRouter);


// Catch-all route to serve React index.html
// app.get("*", (req, res) => {
//     res.sendFile(path.join(__dirname, "../frontend/build", "index.html"));
// });


app.listen(PORT, () => console.log(`Server successfully started at PORT : ${PORT}`));
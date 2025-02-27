const express = require("express");
const multer = require("multer");
const mongoose = require("mongoose");
const cors = require("cors");
const {spawn} = require("child_process");
const {path} = require("path")

require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5173;

// middleware
app.use(cors());
app.use(express.json()); //  handle json data
app.use(express.urlencoded({extended : false}));


mongoose
    .connect("mongodb://127.0.0.1:27017/resume")
    .then((e) => console.log("MongoDB connected"));

// Serve Frontend (after build)
app.use(express.static(path.join(__dirname, "../frontend/build")));

// app.get('/', async (req,res) => {
//     res.render("../frontend/src/main");
// })

// Catch-all route to serve React index.html
app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "../frontend/build", "index.html"));
});




const upload = multer({dest : '../frontend/'});

// app.post()


app.listen(PORT, () => console.log(`Server successfully started at PORT : ${PORT}`));
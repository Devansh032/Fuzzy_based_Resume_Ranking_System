const express = require("express");
const multer = require("multer");
const mongoose = require("mongoose");
const {spawn} = require("child_process");

const app = express();
const PORT = 8000;

mongoose
    .connect("mongodb://127.0.0.1:27017/resume")
    .then((e) => console.log("MongoDB connected"));

app.use(express.urlencoded({extended : false}));


// app.get('/', async (req,res) => {
//     res.render("../frontend/app");
// })



const upload = multer({dest : '../frontend/'});

// app.post()


app.listen(PORT, () => console.log(`Server successfully started at PORT : ${PORT}`));
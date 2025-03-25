import express from 'express';
import multer from 'multer';
import addResume from '../Controllers/resumeController.js';

const resumeRouter = express.Router();

//Image Storage Engine
const storage = multer.diskStorage({
    destination:"upload_job_desc",
    filename : (req,res,cb) => {
        return cb(null,`${Date.now()}${file.originalname}`);
    }
});

const upload = multer({storage:storage});

resumeRouter.post("/addResume",upload.single("file"),addResume);
// jobRouter.get("/list",);


export default resumeRouter;
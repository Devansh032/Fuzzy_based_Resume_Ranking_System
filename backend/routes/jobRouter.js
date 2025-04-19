import express from 'express';
import multer from 'multer';
import {addJobDescription,listJobDescription} from '../Controllers/jobDescriptionController.js';
import fs from 'fs';
const jobRouter = express.Router();



const uploadDir = 'upload_job_desc';
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}


//Image Storage Engine
const storage = multer.diskStorage({
    destination: uploadDir,
    filename : (req,file,cb) => {
        return cb(null,`${Date.now()}${file.originalname}`);
    }
});

const upload = multer({
    storage: storage,
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Only PDF files are allowed'), false);
        }
    }
});

jobRouter.post("/addjob",upload.single("job_description"),addJobDescription);
jobRouter.get("/list",listJobDescription);


export default jobRouter;
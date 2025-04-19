import express from 'express';
import multer from 'multer';
import fs from 'fs';
import path from 'path';
import addResume from '../Controllers/resumeController.js';
const resumeRouter = express.Router();

const uploadDir = 'upload_resume';
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
    destination: uploadDir, 
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
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

resumeRouter.post('/addResume', upload.single('resume'), addResume);

export default resumeRouter;

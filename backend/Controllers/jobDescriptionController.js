import axios from "axios";
// import resumeModel from "../models/resumeModel";
import fs from 'fs';
import {spawn} from 'child_process';
import jobDescriptionModel from "../models/jobDescriptionModel.js";
import path from "path";
import { error } from "console";


import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const addJobDescription = async (req, res) => {
    console.log("✅ Request reached /addJobDescription route!"); // Debug log

    if (!req.file) {
        return res.status(400).json({ success: false, message: "No file uploaded or invalid file type" });
    }

    try {
        const jobDescriptionpath = req.file.path; 
        const resumePath = req.body.resume_path || "null";

        console.log("📜 Job Description:", jobDescriptionpath);
        console.log("📜 resumepath:", resumePath);

        const scriptPath = "C:\\Users\\Admin\\Desktop\\AVI\\CODING\\PROJECTS\\Resume_Ranking_System\\backend\\python_scripts\\process.py";

        const process_job_description = spawn("python", [scriptPath,"process_job_description", resumePath, jobDescriptionpath]);
        
        let job_description = "";

                
        process_job_description.stdout.on("data", (data) => {
            // console.log(data.toString()); // Just for logs
        });

        process_job_description.stdout.on("end", async () => {
            try {
                const filePath = path.join(__dirname, "../temp_job_desc.json");

                if (!fs.existsSync(filePath)) {
                    throw new Error("JSON file not found");
                }

                const fileData = fs.readFileSync(filePath, "utf-8");
                const parsedJobDescription = JSON.parse(fileData.trim());

                console.log("✅ Parsed Job Description:", parsedJobDescription);

                const jobDescription = await jobDescriptionModel.create({
                    jobTitle: parsedJobDescription.jobTitle,
                    jobSkills: parsedJobDescription.jobSkills
                });

                console.log("📌 Successfully saved to MongoDB:", jobDescription);

                // Optionally delete the temp file
                fs.unlinkSync(filePath);
            } catch (error) {
                console.error("❌ JSON Parsing or MongoDB Insertion Error:", error);
            }
        });
        process_job_description.stderr.on("data", (error) => {
            console.error(`Error: ${error}`);
        });
        
        process_job_description.on("close", (code) => {
            console.log(`Python process exited with code ${code}`);
        });

        
        
        // Example response
        res.json({ success: true, message: "job Description uploaded successfully", file: req.file.filename, path: jobDescriptionpath });

    } catch (err) {
        console.error("❌ Error processing resume:", err);
        res.status(500).json({ success: false, message: "Server error while processing the resume" });
    }
};

const listJobDescription = async (req,res) => {
    try{
        const jobs = await jobDescriptionModel.find({},"jobTitle _id");
        res.json(jobs);

    }
    catch(err){
        console.log({error:"failed to fetch job desc."});
    }
};

export {addJobDescription,listJobDescription};
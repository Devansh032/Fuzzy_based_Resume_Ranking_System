import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import jobDescriptionModel from "../models/jobDescriptionModel.js";
import resumeModel from "../models/resumeModel.js";

// Recreate __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const addResume = async (req, res) => {
    console.log("✅ Request reached /addResume route!");

    if (!req.file) {
        return res.status(400).json({ success: false, message: "No file uploaded or invalid file type" });
    }

    try {
        const resumePath = req.file.path;
        const jobDescription_req = req.body.job_description;
        const parsedJobDescription = JSON.parse(jobDescription_req);
        const jobDescription = await jobDescriptionModel.findById(parsedJobDescription._id, "jobSkills");

        console.log("📄 Uploaded Resume Path:", resumePath);
        console.log("📜 Job ID:", parsedJobDescription._id);
        console.log("📜 Job Title:", parsedJobDescription.jobTitle);
        console.log("📜 Job skills:", jobDescription.jobSkills);

        const scriptPath = "C:\\Users\\Admin\\Desktop\\AVI\\CODING\\PROJECTS\\Resume_Ranking_System\\backend\\python_scripts\\process.py";

        // Call Python script and generate temp_resume.json
        const process_resume = spawn("python", [scriptPath, "process_resume", resumePath, JSON.stringify(jobDescription.jobSkills)]);

        process_resume.stdout.on("data", (data) => {
            console.log(`📥 Python says: ${data.toString()}`);
        });

        process_resume.stdout.on("end", async () => {
            try {
                const filePath = path.join(__dirname, "../temp_resume.json");

                if (!fs.existsSync(filePath)) {
                    throw new Error("Resume JSON file not found");
                }

                const fileData = fs.readFileSync(filePath, "utf-8");
                const parsedResumeData = JSON.parse(fileData.trim());

                // console.log("✅ Parsed Resume Data:", parsedResumeData);

                const fuzzylogicPath = "C:\\Users\\Admin\\Desktop\\AVI\\CODING\\PROJECTS\\Resume_Ranking_System\\backend\\python_scripts\\fuzzy_logic.py";

                const rank_cal = spawn("python", [fuzzylogicPath, "process_candidate",JSON.stringify(parsedJobDescription.jobTitle), JSON.stringify(jobDescription.jobSkills)]);
                let rank_cal_data = "";
                rank_cal.stdout.on("data", (data) => {
                    rank_cal_data += data.toString();
                });

                rank_cal.stdout.on("end", async () => {
                    try{

                        const newResume = await resumeModel.create({
                            candidate_name: parsedResumeData.candidate_name,
                            email: parsedResumeData.email,
                            phone: parsedResumeData.phone,
                            rank: rank_cal_data,
                            skills: parsedResumeData.skills,
                            experience_years: parsedResumeData.total_experience,
                            certifications: parsedResumeData.certifications,
                            project_category : parsedResumeData.project_category,
                            // parsed_text: parsedResumeData.resume_text,
                            resume_pdf: {
                                file_name: parsedResumeData.file_name,
                                uploaded_at: new Date()
                            }
                        });

                        console.log(rank_cal_data);
        
                        console.log("📌 Successfully saved resume to MongoDB: and start of process candidate : ");
        
                        
                        console.log("📈 Rank calculation completed.");
                        // Optional: delete temp file
                        fs.unlinkSync(filePath);
                    }
                    catch (error) {
                        console.error("❌ Error during rank calculation:", error);
                    }
                    
                });

                rank_cal.stderr.on("data", (error) => {
                    console.error(`❌ Python Error: ${error}`);
                });

                rank_cal.on("close", (code) => {
                    console.log(`⚙️ Python process exited with code ${code}`);
                });

            } catch (error) {
                console.error("❌ JSON Parsing or MongoDB Insertion Error:", error);
            }
        });

        process_resume.stderr.on("data", (error) => {
            console.error(`❌ Python Error: ${error}`);
        });

        process_resume.on("close", (code) => {
            console.log(`⚙️ Python process exited with code ${code}`);
        });

        console.log("✅ Resume processing completed.");


        res.json({ success: true, message: "Resume uploaded successfully", file: req.file.filename, path: resumePath });

    } catch (err) {
        console.error("❌ Error processing resume:", err);
        res.status(500).json({ success: false, message: "Server error while processing the resume" });
    }
};

export default addResume;

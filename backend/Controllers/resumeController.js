import axios from "axios";
// import resumeModel from "../models/resumeModel";
import fs from 'fs';
import {spawn} from 'child_process';

const addResume = async (req,res) => {
    const resumeData = req.body.resume;
    const jobDescription = req.body.job_description;
    
    // const process_resume = spawn("python", ['../python_scripts/analyzer.py']);
    // data = process_resume(resume_path,JobDescription.objects.get(id=job_id).job_description)
    console.log(req);
    
    try{
        // await food.save();
        res.json({success:true,message:"Food Added"});
    }catch (err){
        console.log(err);
        // console.log(req);
        res.json({success:false,message:"Error"});
    }   

}

export default addResume;
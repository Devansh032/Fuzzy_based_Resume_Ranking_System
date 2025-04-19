import {mongoose } from 'mongoose';
const jobDescriptionSchema = new mongoose.Schema({
    jobTitle: { type: String, required: true },
    jobSkills: { type: Object, required: true },
});

const jobDescriptionModel = mongoose.models.jobDescription || mongoose.model("jobDescription", jobDescriptionSchema);
export default jobDescriptionModel;
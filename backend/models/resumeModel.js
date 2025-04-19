import {mongoose } from 'mongoose';
const resumeSchema = new mongoose.Schema({
    candidate_name : {
        type : String,
        required : true
    },
    email : {
        type : String,
        required : true,
    },
    phone : {
        type : String,
    },
    rank:{
        type : String,
    },
    skills: {
        low: [String],
        medium: [String],
        high: [String]
      },
    experience_years : {
        type : Number
    },
    certifications : {
        type : [String]
    },
    parsed_text : {
        type : String
    },
    resume_pdf : {
        file_id : {
            type : mongoose.Schema.Types.ObjectId,
            ref : "fs.files" 
        },
        file_name : {
            type : String,
        },
        uploaded_at : {
            type : Date,
            default : Date.now()
        }
    }
});

const resumeModel = mongoose.models.resume || mongoose.model("resume",resumeSchema);

export default resumeModel;
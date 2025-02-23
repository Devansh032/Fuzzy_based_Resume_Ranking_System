const {Schema,model, default: mongoose} = require("mongoose");

const resumeSchema = new Schema({
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
    skills : {
        type : [String]
    },
    experience_years : {
        type : Number
    },
    education : {
        type : String
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
            ref : "fs.files" //GridFs reference
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

const Resume = model("resume",resumeSchema);

module.exports = Resume;
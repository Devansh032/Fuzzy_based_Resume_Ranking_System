import React, { useEffect, useState } from 'react'
import { assets } from '../../assets/admin_assets/assets'
import './Add.css';
import { toast } from 'react-toastify';
import axios from 'axios';

interface MyModel {
    id: number;
    name: string;
    // Add other fields based on your Django model
}

interface jobSchema{
    _id : string,
    jobTitle : string
}

interface DropdownProps {
    jobDescriptions: jobSchema[];
    setSelectedJob: React.Dispatch<React.SetStateAction<string>>;
}


const Add : React.FC< {url:string}> = ({url}) => {

    const [jobDescriptions, setJobDescriptions] = useState<jobSchema[]>([]);
    const [selectedJob, setSelectedJob] = useState("");
    const [pdfFile, setPdfFile] = useState<File | null>(null);

    useEffect(() => {
        fetch("http://localhost:4000/api/jobs/list") // Adjust API URL as needed
            .then(response => response.json())
            .then(data => setJobDescriptions(data))
            .catch(error => console.error("Error fetching jobs:", error));
    }, []);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setPdfFile(e.target.files[0]);
            console.log("Selected PDF:", e.target.files[0]);
        }
    };


    const onSubmitHandler = async (event : React.FormEvent) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('job_description',selectedJob);
        if(pdfFile){
            formData.append('resume',pdfFile);
        }
        console.log("✅ Request frontend reached /addResume route!"); // Debug log
        const response = await axios.post(`${url}/api/resume/addResume`,formData);
        console.log(response);
        if(response.data.status){
            toast.success(response.data.message);
        }
        else{
            toast.error(response.data.message);
        }
    };

    


    const JobDescriptionDropdown: React.FC<DropdownProps> = ({ jobDescriptions, setSelectedJob }) => {
        return (
            <select onChange={(e) => setSelectedJob(e.target.value)} required>
                <option value="">Select a Job Description</option>
                {jobDescriptions.map((job) => (
                    <option key={job._id} value={JSON.stringify(job)}>
                        {job.jobTitle}
                    </option>
                ))}
            </select>
        );
    };


    return (
        <div className='add'>
            <form className='flex-col' onSubmit={(e) => onSubmitHandler(e)} >
                <div className="add-pdf-upload flex-col">
                    <p>Select Job Description</p>
                    <JobDescriptionDropdown
                        jobDescriptions={jobDescriptions}
                        setSelectedJob={setSelectedJob}
                    />
                </div>
                <div className="add-pdf-upload flex-col">
                    <p>Upload resume</p>
                    <label className='upload-box' htmlFor='pdf-upload'>
                        <img src={assets.upload_area} alt='' />
                    </label>
                    <input onChange={(e) => handleFileChange(e)}
                    type='file' 
                    id='pdf-upload' 
                    hidden 
                    accept='.pdf'
                    required/>
                </div>
                <button type='submit' className='add-btn'>ADD</button>
            </form>
        </div>
    )
}
export default Add

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

const Add : React.FC< {url:string}> = ({url}) => {

    const [jobDescription,setJobDescription] = useState<string> ("1");
    const [pdfFile, setPdfFile] = useState<File | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setPdfFile(e.target.files[0]);
            console.log("Selected PDF:", e.target.files[0]);
        }
    };


    const onSubmitHandler = async (event : React.FormEvent) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('job_description',jobDescription);
        if(pdfFile){
            formData.append('resume',pdfFile);
        }
        const response = await axios.post(`${url}/api/resume/addResume`,formData);
        console.log(response);
        if(response.data.status){
            toast.success(response.data.message);
        }
        else{
            toast.error(response.data.message);
        }
    }

  return (
        <div className='add'>
            <form className='flex-col' onSubmit={(e) => onSubmitHandler(e)} >
                <div className="add-pdf-upload flex-col">
                    <p>Select Job Description</p>
                    <select onChange={(e) => setJobDescription(e.target.value)} required>
                        const jobDescription = 
                    </select>
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

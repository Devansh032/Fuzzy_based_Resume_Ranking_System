import axios from 'axios';
import React, { useState } from 'react'
import { toast } from 'react-toastify';
import { assets } from '../../assets/admin_assets/assets';

const Addjob : React.FC< {url:string}> = ({url}) => {
  const [jobPdfFile,setJobPdfFile] = useState<File | null > (null);
   
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
          setJobPdfFile(e.target.files[0]);
            console.log("Selected PDF:", e.target.files[0]);
        }
    };

    const onSubmitHandler = async (event : React.FormEvent) => {
        event.preventDefault();
        const formData = new FormData();
        
        if(jobPdfFile){
            formData.append('job_description',jobPdfFile);
        }
        console.log("✅ Request frontend reached /addjob route!"); // Debug log
        const response = await axios.post(`${url}/api/jobs/addjob`,formData);
        console.log(response);
        if(response.data.success){
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
                    <p>Upload Job Description</p>
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

export default Addjob

import { candidateFormSchema } from "@/lib/validations";
import { z } from "zod";

type CandidateData = z.infer<typeof candidateFormSchema>;

export const handleCandidateSave = async (data: CandidateData) => {
    const formdata = new FormData();
    
    formdata.append("full_name", data.full_name);
    formdata.append("email", data.email);
    formdata.append("date_of_birth", data.date_of_birth.toISOString().split('T')[0]);
    formdata.append("years_of_experience", data.years_of_experience.toString());
    formdata.append("department_id", data.department_id);
    if (data.resume) {
        formdata.append("resume", data.resume);
    }

    const requestOptions = {
        method: "POST",
        body: formdata,
    };

    const response = await fetch("http://localhost:8000/vault/candidate/register", requestOptions);
    const jsonResponse = await response.json();
    
    if (response.status === 400) {
        throw jsonResponse.error;
    }
    
    return data;
}

export const handleCandidateList = async (page: number) => {
    
    const myHeaders = new Headers();
    myHeaders.append("X-ADMIN", "1");

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
    };

    const response = await fetch(`http://localhost:8000/vault/candidates?page=${page}`, requestOptions);
    const jsonResponse = await response.json();

    if (response.status === 400) {
        throw jsonResponse.error;
    }

    return jsonResponse;
}

export const handleCandidateResumeDownload = async (candidateId: string) => {
    const myHeaders = new Headers();
    myHeaders.append("X-ADMIN", "1");

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
    };

    const response = await fetch(`http://localhost:8000/vault/candidate/${candidateId}/resume`, requestOptions);
    
    if (!response.ok) {
        const jsonResponse = await response.json();
        throw jsonResponse.error;
    }

    const blob = await response.blob();
    const filename = response.headers.get('content-disposition')?.split('filename=')[1]?.replace(/"/g, '');

    
    return {
        url: URL.createObjectURL(blob),
        filename: filename
    };
}
import { z } from "zod";

export const candidateFormSchema = z.object({
    full_name: z.string().min(1, { message: "Full name is required" }),
    email: z.string().email({ message: "Invalid email address" }),
    date_of_birth: z.date().max(new Date(), { message: "Date of birth cannot be in the future" }),
    years_of_experience: z.number().min(1, { message: "Years of experience is required" }),
    department_id: z.enum(["1", "2", "3", "4", "5", "6"], {
        errorMap: () => ({ message: "Please select a valid department" })
    }),
    resume: z.instanceof(File, { message: "Resume is required" }),
});
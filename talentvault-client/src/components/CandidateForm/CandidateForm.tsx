import { useEffect } from "react";
import { useForm } from "react-hook-form"
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod"
import { toast } from "sonner";

import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import useSubmit from "@/hooks/useSubmit";
import { candidateFormSchema } from "@/lib/validations";

const CandidateForm = () => {
  	const form = useForm<z.infer<typeof candidateFormSchema>>({
		resolver: zodResolver(candidateFormSchema),
		defaultValues: {
			full_name: "",
			email: "",
			date_of_birth: new Date(),
			years_of_experience: 1,
			department_id: "1",
			resume: undefined,
		},
	});

	const { mutate: submit, isPending, isError, isSuccess, error } = useSubmit();

	const onSubmit = async (data: z.infer<typeof candidateFormSchema>) => {
		await submit(data);

	};

	useEffect(() => {
		if (isSuccess) {
			toast.success('Candidate registered successfully!');
			form.reset();
		}
		if (isError) {
			toast.error(JSON.stringify(error));
		}
	}, [isError, isSuccess, error]);

	return (
		<div className="flex justify-center items-center min-h-screen bg-gray-300 p-4">
			<div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
				<h1 className="text-2xl font-bold text-center mb-6">Candidate Registration</h1>
				<Form {...form}>
					<form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
						<FormField
							control={form.control}
							name="full_name"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Full Name</FormLabel>
									<FormControl>
										<Input
											type="text"
											placeholder="Full Name"
											{...field}
											className="w-full"
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>
						<FormField
							control={form.control}
							name="email"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Email</FormLabel>
									<FormControl>
										<Input
											type="email"
											placeholder="Email"
											{...field}
											className="w-full"
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>
						<FormField
							control={form.control}
							name="date_of_birth"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Date of Birth</FormLabel>
									<FormControl>
										<Input
											type="date"
											placeholder="Date of Birth"
											value={field.value instanceof Date ? field.value.toISOString().split('T')[0] : ''}
											onChange={(e) => field.onChange(new Date(e.target.value))}
											onBlur={field.onBlur}
											name={field.name}
											ref={field.ref}
											className="w-full"
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>
						<FormField
							control={form.control}
							name="years_of_experience"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Years of Experience</FormLabel>
									<FormControl>
										<Input
											type="number"
											placeholder="Years of Experience"
											{...field}
											className="w-full"
											value={field.value}
											onChange={(e) => field.onChange(Number(e.target.value))}
											onBlur={field.onBlur}
											name={field.name}
											ref={field.ref}
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>
						<FormField
							control={form.control}
							name="department_id"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Department</FormLabel>
									<Select onValueChange={field.onChange} defaultValue={field.value}>
										<FormControl>
										<SelectTrigger>
											<SelectValue placeholder="Select a department" />
										</SelectTrigger>
										</FormControl>
										<SelectContent>
											<SelectItem value="1">Engineering</SelectItem>
											<SelectItem value="2">Sales</SelectItem>
											<SelectItem value="3">Marketing</SelectItem>
											<SelectItem value="4">Human Resources</SelectItem>
											<SelectItem value="5">Finance</SelectItem>
											<SelectItem value="6">Operations</SelectItem>
										</SelectContent>
									</Select>
									<FormMessage />
								</FormItem>
							)}
						/>
						<FormField
							control={form.control}
							name="resume"
							render={({ field }) => (
								<FormItem>
									<FormLabel>Resume</FormLabel>
									<FormControl>
										<Input
											type="file"
											placeholder="Resume"
											className="w-full"
											onChange={(e) => {
												if (e.target.files?.[0]) {
													field.onChange(e.target.files[0])
												}
											}}
											onBlur={field.onBlur}
											name={field.name}
											ref={field.ref}
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							)}
						/>
						<Button type="submit" className="w-full cursor-pointer" disabled={isPending}>
							{isPending ? "Submitting..." : "Submit Application"}
						</Button>
					</form>
				</Form>
			</div>
		</div>
	)
}

export default CandidateForm
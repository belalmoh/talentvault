import { useState } from "react";

import useGetCandidates from "@/hooks/useGetCandidates";
import { handleCandidateResumeDownload } from "@/apis";

const Admin = () => {
	const [page, setPage] = useState(1);
	const { data, isLoading, isError, error } = useGetCandidates(page);
	
	const handleDownloadResume = (candidateId: string) => {
		handleCandidateResumeDownload(candidateId).then(({ url, filename }) => {
			const link = document.createElement('a');
			link.href = url;
			link.download = filename || 'resume';
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			URL.revokeObjectURL(url);
		})
	}

	return (
		<div className="flex justify-center items-center min-h-screen bg-gray-300 p-4">
			<div className="w-full max-w-4xl bg-white rounded-lg shadow-lg p-8 flex flex-col h-[70vh]">
				<h1 className="text-2xl font-bold text-center mb-6">Candidate List</h1>
				
				<div className="overflow-auto flex-grow">
					<table className="w-full border-collapse">
						<thead className="sticky top-0 bg-white">
							<tr className="bg-gray-100">
								<th className="px-4 py-2 text-left border-b-2 border-gray-200">Name</th>
								<th className="px-4 py-2 text-left border-b-2 border-gray-200">Email</th>
								<th className="px-4 py-2 text-left border-b-2 border-gray-200">Department</th>
								<th className="px-4 py-2 text-left border-b-2 border-gray-200">Experience</th>
								<th className="px-4 py-2 text-left border-b-2 border-gray-200">Actions</th>
							</tr>
						</thead>
						<tbody>
							{data?.candidates.map((candidate) => (
								<tr key={candidate.id} className="hover:bg-gray-50">
									<td className="px-4 py-3 border-b border-gray-200">{candidate.full_name}</td>
									<td className="px-4 py-3 border-b border-gray-200">{candidate.email}</td>
									<td className="px-4 py-3 border-b border-gray-200">{candidate.department}</td>
									<td className="px-4 py-3 border-b border-gray-200">{candidate.years_of_experience} years</td>
									<td className="px-4 py-3 border-b border-gray-200">
										<button 
											className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm"
											onClick={() => handleDownloadResume(candidate.id)}
										>
											Download Resume
										</button>
									</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>
				
				<div className="mt-6 flex justify-between">
					<button 
						className="bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded disabled:opacity-50"
						disabled={page === 1}
						onClick={() => setPage(page - 1)}
					>
						Previous
					</button>
					<span className="py-2">Page {page} of {data?.total_pages}</span>
					<button 
						className="bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded disabled:opacity-50"
						disabled={page === data?.total_pages}
						onClick={() => setPage(page + 1)}
					>
						Next
					</button>
				</div>
			</div>
		</div>
	)
}

export default Admin;

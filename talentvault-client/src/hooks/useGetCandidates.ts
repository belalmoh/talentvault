import { handleCandidateList } from "@/apis";
import { useQuery } from "@tanstack/react-query";

const useGetCandidates = (page: number) => {
    const { data, isLoading, isError, error } = useQuery({ queryKey: ["candidates", page], queryFn: () => handleCandidateList(page) });

    return { data, isLoading, isError, error };
}

export default useGetCandidates;
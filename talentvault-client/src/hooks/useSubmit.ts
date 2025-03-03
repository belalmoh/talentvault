import { useMutation } from "@tanstack/react-query";
import { handleCandidateSave } from "@/apis";

const useSubmit = () => {
    const mutation = useMutation({
        mutationFn: handleCandidateSave
    })
    return mutation;
}

export default useSubmit;
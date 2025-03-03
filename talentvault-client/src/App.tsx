import { Routes, Route } from "react-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/sonner";

import Home from "./pages/home/Home";
import Admin from "./pages/admin/Admin";
import Navbar from "./components/Navbar/Navbar";
const queryClient = new QueryClient();

const App = () => {
	return (
		<QueryClientProvider client={queryClient}>
			<Navbar />
			<Routes>
				<Route index element={<Home />} />
				<Route path="/admin" element={<Admin />} />
			</Routes>
			<Toaster />
		</QueryClientProvider>
	);
};

export default App;

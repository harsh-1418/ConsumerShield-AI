import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import NewComplaint from "./pages/NewComplaint";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/new-complaint" element={<NewComplaint />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
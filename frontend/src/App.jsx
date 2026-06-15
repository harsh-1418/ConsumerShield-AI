import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import NewComplaint from "./pages/NewComplaint";
import CaseInsights from "./pages/CaseInsights";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/new-complaint"
          element={<NewComplaint />}
        />
        <Route
          path="/case-insights"
          element={<CaseInsights />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
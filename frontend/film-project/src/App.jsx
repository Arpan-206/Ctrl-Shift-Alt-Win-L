import Timeline from "./pages/timeline"
import {BrowserRouter, Routes, Route} from "react-router-dom"
function App() {
  

  return (
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<div />} />
            <Route path="/timeline" element={<Timeline />} />
          </Routes>
      </BrowserRouter>
  )
}

export default App

import Timeline from "./pages/timeline"
import Test from "./pages/test"
import {BrowserRouter, Routes, Route} from "react-router-dom"
import Discovery from "./pages/discovery";
import HomePage from "./pages/home";
import FilmLogger from "./pages/FilmLogger";

function App() {
  

  return (
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage/>} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/discovery" element={<Discovery/>} />
            <Route path="/log-film" element={<FilmLogger/>} />
          </Routes>
      </BrowserRouter>
  )
}

export default App

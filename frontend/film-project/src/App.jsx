import Timeline from "./pages/timeline";
import {BrowserRouter, Routes, Route} from "react-router-dom"
import Discovery from "./pages/discovery";
import HomePage from "./pages/home";
import FilmLogger from "./pages/FilmLogger";
import LoginPage from "./pages/login";
import AboutPage from "./pages/About";

function App() {
  

  return (
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage/>} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/discovery" element={<Discovery/>} />
            <Route path="/log-film" element={<FilmLogger/>} />
            <Route path="/login" element={<LoginPage/>} />
            <Route path="/about" element={<AboutPage className="w-[100vw]"></AboutPage>}/>
          </Routes>
      </BrowserRouter>
  )
}

export default App

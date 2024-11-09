import "./styles/home.css"
import {useRef} from "react"
function HomePage()
{
    
    const actionbtn = document.querySelector('.actionbtn');
    const navbar = document.querySelector('.navbar');
    const banner = document.querySelector('.banner');
/*
    actionbtn.addEventListener('click', () => {
        actionbtn.classList.toggle('active');
        navbar.classList.toggle('active');
        banner.classList.toggle('active');
    })*/

    return(
        <>
        <div className="container">
            <div className="stars"></div>
            <div onClick={() => {
        actionbtn.classList.toggle('active');
        navbar.classList.toggle('active');
        banner.classList.toggle('active');}}className="actionbtn">
        <span className="fas fa-light fa-star"></span>

    </div>

    <ul className="navbar">
        <li><a href="https://localhost:44316/Home.html#">Home</a></li>
        <li><a href="#">About</a></li>
        <li><a href="https://localhost:44316/MyFilms.html">My Films</a></li>
        <li><a href="https://localhost:44316/MyJourney.html">Log a Film</a></li>
        <li><a href="#">My Journey</a></li>
        <li><a href="#">Discover</a></li>
    </ul>



    <div className="banner">
        <div className="vidbg">
            <video autoPlay muted loop id="bg-video">
                <source src="Hollywood Blur.mp4" type="video/mp4"></source>
                Your browser does not support the video tag.
            </video>
        </div>
        <div className="text">
            <h1>Film Odyssey</h1>
            <p className="info">Film Journey is your gateway to exploring the cinematic universe across time. Log the films you've watched, discover new titles, and trace your viewing history on a personalized timeline. Whether you're diving into classic films, modern blockbusters, or hidden gems, Film Journey helps you reflect on your adventures through the world of cinema and uncover new destinations to explore.</p>
            <div className="btns">
                <a href="#">Discover Films</a>
                <a href="#">Log a film</a>
            </div>
        </div>
    </div>
</div>

        </>
    );
}

export default HomePage;
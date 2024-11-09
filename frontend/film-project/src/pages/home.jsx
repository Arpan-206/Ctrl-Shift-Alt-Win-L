import "./styles/home.css"

import {useRef, useState, useEffect} from "react"
function HomePage()
{
    const [sideMenuState, setSideMenuState] = useState(false);
    useEffect(() => {createStars();}, [])
        
    return(
        <>
            <div className="absolute w-[100vw] top-[0px] h-[10vh] z-50 bg-[#FFFFFF]">
                    
            </div>
            <div className="container h-[90vh]">
                
                <button className="actionbtn" onClick={()=>{setSideMenuState(!sideMenuState)}}></button>
                <div className="stars"></div>
                <div onClick={() => {setSideMenuState(!sideMenuState); console.log(sideMenuState)}}>
                    <span className="fas fa-light fa-star"></span>
                </div>

                <ul className={sideMenuState==false ? "navbar": "navbar.active"}>
                    <li><a href="https://localhost:44316/Home.html#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="https://localhost:44316/MyFilms.html">My Films</a></li>
                    <li><a href="https://localhost:44316/MyJourney.html">Log a Film</a></li>
                    <li><a href="#">My Journey</a></li>
                    <li><a href="#">Discover</a></li>
                </ul>
                <div className={sideMenuState==false ? "banner" : "banner.active"}>
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

function createStars() {
    const stars = document.querySelector('.stars');
    const count = 200; // Number of stars
    if(stars==null) return;
    for (let i = 0; i < count; i++) {
        const star = document.createElement('div');
        
        star.classList.add('star');
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.animationDelay = `${Math.random() * 4}s`;
        stars.appendChild(star);
    }
}



// Reveal timeline items as the user scrolls down
document.addEventListener('DOMContentLoaded', function () {
    const timelineItems = document.querySelectorAll('.timeline-item');

    const revealItems = () => {
        const triggerBottom = window.innerHeight / 5 * 4;

        timelineItems.forEach(item => {
            const itemTop = item.getBoundingClientRect().top;
            if (itemTop < triggerBottom) {
                item.classList.add('show');
            }
        });
    };

    window.addEventListener('scroll', revealItems);
    revealItems(); // Initial check on page load
});
export default HomePage;
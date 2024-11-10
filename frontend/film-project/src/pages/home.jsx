import "./styles/home.css"
import Header from "./components/Header";
import {useRef, useState, useEffect} from "react"
function HomePage()
{
    useEffect(() => {createStars();}, [])
        
    return(
        <>
            <div className="w-[100vw] h-[100vh] absolute top-[0px]">
                <Header className="absolute top-[0px]"></Header>
                <div className="stars"></div>
                <div className="absolute w-[100%] mt-[150px] text-center flex justify-center">
                    <div className="h-[100%] w-[80%] ">
                        <h1>Film Odyssey</h1>
                        <p className="info">Film Odyssey is your gateway to exploring the cinematic universe across time. Log the films you've watched, discover new titles, and trace your viewing history on a personalized timeline. Whether you're diving into classic films, modern blockbusters, or hidden gems, Film Journey helps you reflect on your adventures through the world of cinema and uncover new destinations to explore.</p>
                        <div className="btns">
                            <a href="/timeline">Timeline</a>
                            <a href="/discovery">Discovery</a>
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
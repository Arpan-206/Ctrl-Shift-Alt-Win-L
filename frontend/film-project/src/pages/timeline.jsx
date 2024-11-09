import {useEffect} from "react";
import "./styles/timeline.css";
export default function Timeline()
{
    useEffect(()=>{
        createStars();
    },[]);
    return (
        <>
            <div className="container">
        <div className="stars"></div>
        <div className="actionbtn">
            <span className="fas fa-light fa-star"></span>
        </div>


        {/*<!-- Title and Caption -->*/}
        <h1 className="timeline-title">My Film Journey</h1>
        <p className="timeline-caption">Explore the films that shaped your journey through time</p>

        {/*<!-- Vertical Timeline Section -->*/}
        <section className="vertical-timeline">
            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2008</h2>
                    <p>Marvel Studios releases *Iron Man*, kicking off the Marvel Cinematic Universe (MCU) and changing the landscape of superhero films forever.</p>
                    <img src="SATSV.jpg" alt="Iron Man" class="film-image"></img>
                </div>
            </div>

            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2010</h2>
                    <p>*Inception*, directed by Christopher Nolan, leaves audiences questioning reality with its mind-bending mix of dreams and action-packed sci-fi.</p>
                    <img src="SATSV.jpg" alt="Inception" class="film-image"></img>
                </div>
            </div>

            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2014</h2>
                    <p>*Interstellar* takes viewers on a journey through space and time, exploring the boundaries of physics, love, and survival.</p>
                    <img src="SATSV.jpg" alt="Interstellar" class="film-image"></img>
                </div>
            </div>

            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2019</h2>
                    <p>*Avengers: Endgame* smashes box office records and becomes a cultural phenomenon, bringing a satisfying conclusion to over a decade's worth of superhero storytelling.</p>
                    <img src="SATSV.jpg" alt="Avengers: Endgame" class="film-image"></img>
                </div>
            </div>

            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2021</h2>
                    <p>*Dune*, directed by Denis Villeneuve, brings Frank Herbert’s sci-fi epic to the big screen with stunning visuals and a star-studded cast.</p>
                    <img src="SATSV.jpg" alt="Dune" class="film-image"></img>
                </div>
            </div>

            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2022</h2>
                    <p>*The Batman*, directed by Matt Reeves, offers a darker, more grounded take on Gotham's Caped Crusader.</p>
                    <img src="SATSV.jpg" alt="The Batman" class="film-image"></img>
                </div>
            </div>

            <div className="timeline-item">
                <div className="timeline-content">
                    <h2>2023</h2>
                    <p>*Oppenheimer*, directed by Christopher Nolan, explores the life of J. Robert Oppenheimer and the creation of the atomic bomb.</p>
                    <img src="SATSV.jpg" alt="Oppenheimer" class="film-image"></img>
                </div>
            </div>
        </section>
    </div>
        </>
    );
}
function createStars() {
    const stars = document.querySelector('.stars');
    const count = 200; // Number of stars

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
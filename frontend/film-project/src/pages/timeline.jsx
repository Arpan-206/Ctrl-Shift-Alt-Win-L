import {useEffect} from "react";
import "./styles/timeline.css";
import Header from "./components/Header";
import GetTimeLine from "../API/Timeline";
export default function Timeline()
{
    useEffect(()=>{
        createStars();
        GetTimeLine();
        
    },[]);
    let movieData = [
        {
            title: "Paddington",
            year: "2014",
            plot: "The bessst.",
            date_watched: "release date",
            poster: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3aFkoa9hig8TVAglf01TXnyjPGWMeZiXeyw&s",
        },
        {
            title: "TEST 2",
            year: "1000",
            plot: "PLOT2",
            date_watched: "N/A",
            poster: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS3aFkoa9hig8TVAglf01TXnyjPGWMeZiXeyw&s",
        }
    ]
    
    return (
        <>
            <div className="containerf w-[100vw] text-center">
            
                <div className="stars"></div>
                <div className="actionbtn">
            <span className="fas fa-light fa-star"></span>
        </div>


        {/*<!-- Title and Caption -->*/}
        <Header></Header>
        
        <h1 className="timeline-titleg text-center relative">My Film Journey</h1>
        <p className="timeline-caption font-Noto-Sans">Explore the films that shaped your journey through time</p>

        {/*<!-- Vertical Timeline Section -->*/}
        <section className="vertical-timeline">
            {movieData.map((movie, index) => {
                return(
                    <div className="timeline-item">
                        <div className="timeline-content">
                            <h2 className="date-item">{movie.date_watched}</h2>
                            <p>{movie.plot}</p>
                            <img src={movie.poster} alt="Iron Man" class="film-image"></img>
                        </div>
                    </div>
                )
            }
            )}
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
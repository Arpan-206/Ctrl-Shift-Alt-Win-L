import {useEffect, useState} from "react";
import "./styles/timeline.css";
import Header from "./components/Header";
import GetTimeLine from "../API/Timeline";
export default function Timeline()
{
    const [data, setData] = useState([]);
    useEffect(()=>{
        createStars();
        GetTimeLine().then(response => {
            data = setData(response);
            
            
        });
    },[]);
    
    return (
        <>
            <div className="bg-[#242424] absolute top-[0px] w-auto text-center">
            
                <div className="stars"></div>
        {/*<!-- Title and Caption -->*/}
        <Header className="absolute top-[0px]"></Header>
        {console.log(data)}
        <h1 className="timeline-titleg text-center relative">My Film Journey</h1>
        <p className="timeline-caption font-Noto-Sans">Explore the films that shaped your journey through time</p>

        {/*<!-- Vertical Timeline Section -->*/}
        <section className="vertical-timeline">
            {data!=null && data.map((movie, index) => {
                return(
                    
                    <div className="timeline-item">
                        <div className="timeline-content">
                            <h3 className="text-center text-[35px] mt-[5px]">{movie.title}</h3>
                            <h2 className="date-item">{movie.date_watched}</h2>
                            <p>{movie.plot}</p>
                            <img src={movie.poster} alt="Iron Man" className="film-image relative justify-self-center flex"></img>
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
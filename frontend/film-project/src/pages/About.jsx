import "./styles/about.css";
import Header from "./components/Header";
export default function AboutPage()

{
    
    return(
        <div className="container w-[100vw] h-auto overflow-visible">
            <Header className="w-[100vw]"></Header>
        <section className="about-section w-[100vw]">
            <div className="glass-box">
                <h1>About Film Odyssey</h1>
                <p>
                    <strong>Film Odyssey</strong> is your gateway to exploring the world of cinema across time and space. Our mission is to create a personalized journey for film lovers to log their viewing experiences and discover new films from around the globe.
                </p>
                <p>
                    Whether you're revisiting classic films or discovering new cinematic gems, our platform helps you track your journey through genres, time periods, and settings. With an interactive timeline and custom recommendations, Film Odyssey is your ultimate guide to the past, present, and future of cinema.
                </p>
                <p>
                    Join us on this cinematic adventure as we explore the rich history of film, one movie at a time.
                </p>

                <div className="features-container">

                    <div className="feature-item">
                        <i className="fas fa-film"></i>
                        <h3>My Films</h3>
                        <p>Revisit your collection of logged films anytime. Whether you're looking to rewatch a favorite or reflect on your viewing history, it's all here!</p>
                    </div>

                    <div className="feature-item">
                        <i className="fas fa-edit"></i>
                        <h3>Log a Film</h3>
                        <p>Just finished a film? Log it here and see it instantly added to your timeline. Keep track of every adventure through time.</p>
                    </div>

                    <div className="feature-item">
                        <i className="fas fa-history"></i>
                        <h3>My Journey</h3>
                        <p>Take a trip back in time and explore your movie-watching timeline. Reflect on how each film has shaped your unique cinematic journey.</p>
                    </div>

                    <div className="feature-item">
                        <i className="fas fa-search"></i>
                        <h3>Discover</h3>
                        <p>Not sure what to watch next? Let us curate the perfect recommendations based on your viewing history and preferences.</p>
                    </div>

                </div>
            </div>
        </section>
        </div>

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
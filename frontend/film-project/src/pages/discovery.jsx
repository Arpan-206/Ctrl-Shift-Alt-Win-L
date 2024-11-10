import Header from "./components/Header";
import {Card, CardBody, Spacer, Image} from "@nextui-org/react"
import {useState, useEffect} from "react"
import GetDiscoveryData from "../API/Discovery";
import "./styles/glass.css";
export default function Discovery()
{
    const [data, setData] = useState(null);
    useEffect(() => {
        GetDiscoveryData().then(respone=>{
            setData(respone);
            console.log(response);
        })
        
    }, []);
    return(
        
        <div className="absolute top-[0px] w-[100vw] h-[100vh] ">
            <Header></Header>
            <div className="block">
                <h1 className = "text-[50px] w-[100vw]">Discovery</h1>
                {data==null ? <div className="">
                    <h3 className="text-center text-[#505050]">Loading</h3>
                </div> :
                (data!=null && data.map((item, index) => {
                    return(
                        <div>
                        <Card className="inline-block glass relative w-[80%] left-[10%] mb-[40px] opacity-10 bg-white">
                            <CardBody className="h-[300px] inline-block">
                                
                                <h3 className="text-[50px] text-center">{item.Title}</h3>
                                <span>
                                    <Image src={item["Poster"]} className= "m-auto w-[300px] ml-[20px]"></Image>
                                    <h3 className="text-[25px]">
                                        {item.Reason}
                                    </h3>
                                </span>
                            </CardBody>
                        </Card>
                        <Spacer></Spacer>
                        </div>
                    )
                }))}
                
                </div>
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
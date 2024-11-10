import Header from "./components/Header"
import {Modal, ModalContent, ModalHeader, Input, ModalBody, DateInput, Textarea, Button, Autocomplete, AutocompleteItem} from "@nextui-org/react"
import {useRef, useState, useEffect} from "react"
import SubmitItems from "../API/FilmLogger"
import { GetItems } from "../API/FilmLogger"
import "./styles/home.css";
export default function FilmLogger()
{
    let search = "";
    const [searchResult, setSearchResult] = useState([]);
    let titleField = useRef(null);
    let dateField = useRef(null);
    let reviewField = useRef(null);

    useEffect(() => 
        {
            createStars();

        }, [])
    useEffect(() => {
        console.log(search);
        GetItems(search).then(async respone=>{
            setSearchResult(await respone);
        });
    }, [titleField.value]);
    return(
        <div>

            <div className="z-10"></div>
            <Header className="absolute top-[0px]"/>
            <div className="w-[100vw] h-[90vh] mt-[50px] flex justify-center items-center">
            <div className="relative w-[80vw] h-[80vh] inline-block rounded-[30px] shadow-lg bg-[#202020]">
                    <div className="Header w-[100%] ml-[50px] mt-[50px] mb-[50px]">
                        <h1 className="font-semibold text-white text-[30px]">Add a Film</h1>
                    </div>
                    <img src="https://placehold.co/2000x3000" className="absolute ml-[50px] w-[200px] rounded-[15px]"></img>
                    <div className="InputFields ml-[290px] mr-[20px]">
                        <Input ref={titleField} className="mb-[10px]"placeholder="Film Name">
                        </Input>
                        <Button className="relative mr-[50px]" onClick={()=>{GetItems(titleField.current.value).then(async (response)=>{
                            console.log(response);
                            setSearchResult(await response.data[0]);
                            titleField.current.value = await response.data[0];
                        })}}>Search</Button>
                        <Input ref={dateField} className="mb-[10px]"placeholder="Watch Date"></Input>
                        <Textarea ref={reviewField} className="min-h-[300px]" placeholder="Write a review!"></Textarea>
                    </div>
                    <div className="absolute bottom-[20px] right-[50px]">
                        <Button className="mr-[20px]" onClick={()=>{window.open("/")}}>Cancel</Button>
                        <Button onClick={()=>{console.log(dateField.current.value); SubmitItems(titleField.current.value, dateField.current.value, reviewField.current.value, 0)}}className="">Submit</Button>
                    </div>
            </div>
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
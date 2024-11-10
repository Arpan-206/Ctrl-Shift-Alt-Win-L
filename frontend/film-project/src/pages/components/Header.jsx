import "../styles/header.css";
import {useState} from "react"
export default function Header()
{
    const [isLoggedIn, setIsLoggedIn] = useState(true);
    return(
        <>
            <div class="containerf w-full">
                <header class="header">
                    <a href="" class="logo">Film Odyssey</a>

                    {isLoggedIn == false ? <span class="justify-between flex block-inline text-[#FFFFFF] w-[600px]">
                        
                        <a className = "text-[#FFFFFF]" href="/">Home</a>
                        <a className = "text-[#FFFFFF]" href="#">About</a>
                        <a className = "text-[#FFFFFF]" href="/myfilms">My Films</a>
                        <a className = "text-[#FFFFFF]" href="#">Log a Film</a>
                        <a className = "text-[#FFFFFF]" href="/timeline">My Journey</a>
                        <a className = "text-[#FFFFFF]" href="/discovery">Discover</a></span>:
                        <button onClick={()=>{setIsLoggedIn(!isLoggedIn)}}className="btn">Log In</button>}
                    
                </header>
            </div>
        </>
    );
}
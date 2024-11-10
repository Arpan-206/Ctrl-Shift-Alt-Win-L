import "../styles/header.css";
import { useState, useEffect } from "react"
import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "@nextui-org/react";
import GetAPIToken from "../../API/Auth";
export default function Header() {

    ////////////////////////////////ADD LOGOUT BUTTON LATER//////////////////////////////////
    let isAuthenticated = true;
    return (
        <>
            <div class="w-[100vw]">
                <header className="header w-[100vw]">
                    <a href="" className="logo">Film Odyssey</a>

                    <span class="justify-between flex block-inline text-[#FFFFFF] w-[600px] mr-[80px]">

                        <a className="text-[#FFFFFF]" href="/">Home</a>
                        <a className="text-[#FFFFFF]" href="#">About</a>
                        <a className="text-[#FFFFFF]" href="/log-film">Log a Film</a>
                        <a className="text-[#FFFFFF]" href="/timeline">My Journey</a>
                        <a className="text-[#FFFFFF]" href="/discovery">Discovery</a></span>
                    {(localStorage.getItem("username") == null || localStorage.getItem("password") == null)?
                        <Button onClick={() => { window.location.href = '/login' }} className="bg-[#F8F6E7] absolute top-[20px] right-[30px] z-5 w-[80px] h-[40px] text-[#000000]">Log In</Button> :
                        <Button onClick={() => { localStorage.clear(); window.location.reload() }} className="bg-[#F8F6E7] absolute top-[20px] right-[30px] z-5 w-[80px] h-[40px] text-[#000000]">Log Out</Button>}

                </header>
            </div>
        </>
    );
}
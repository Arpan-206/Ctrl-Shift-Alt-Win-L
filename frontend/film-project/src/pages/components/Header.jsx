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
                        <a className="text-[#FFFFFF]" href="/myfilms">My Films</a>
                        <a className="text-[#FFFFFF]" href="/log-film">Log a Film</a>
                        <a className="text-[#FFFFFF]" href="/timeline">My Journey</a>
                        <a className="text-[#FFFFFF]" href="/discovery">Discover</a></span>
                    {(isAuthenticated == false || localStorage.getItem("access_token") != null)?
                        <Button onClick={() => { loginWithRedirect(); }} className="bg-[#F8F6E7] absolute top-[20px] right-[30px] z-5 w-[80px] h-[40px] text-[#000000]">Log In</Button> :
                        <Button onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })} className="bg-[#F8F6E7] absolute top-[20px] right-[30px] z-5 w-[80px] h-[40px] text-[#000000]">Log Out</Button>}

                </header>
            </div>
        </>
    );
}
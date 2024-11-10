import "./styles/home.css"
import Header from "./components/Header";
import {Modal, ModalContent, ModalHeader, Input, ModalBody, DateInput, Textarea, Button, Autocomplete, AutocompleteItem, user} from "@nextui-org/react";

function LoginPage()
{
    return(
        <div className="absolute top-[0px]">
            {localStorage.getItem("username") && localStorage.getItem("password") ? window.location.href = "/" : null}

            <div className="z-10"></div>
            <Header className="absolute top-[0px]"/>
            <div className="w-[100vw] h-[90vh] mt-[50px] flex justify-center items-center">
            <div className="relative w-[80vw] h-[80vh] inline-block rounded-[30px] shadow-lg bg-[#202020]">
                    <div className="Header w-[100%] ml-[50px] mt-[50px] mb-[50px]">
                        <h1 className="font-semibold text-white text-[30px]">Login</h1>
                    </div>
                    <div className="InputFields mx-[10%]">
                        <Input className="mb-[10px]" placeholder="Username"></Input>
                        <Input type="password" className="mb-[10px]" placeholder="Password"></Input>
                    </div>
                    <div className="absolute bottom-[20px] right-[50px]">
                        <Button onClick={()=>{LoginSubmit()}}className="">Submit</Button>
                    </div>
            </div>
        </div>
        </div>
    );
}

function LoginSubmit()
{
    let username = document.querySelector("input[placeholder='Username']").value;
    let password = document.querySelector("input[placeholder='Password']").value;

    fetch("https://watermelon-bpwf.onrender.com/movies/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Basic ${btoa(username + ':' + password)}`
        }
    }).then(response => {
        if(response.status == 401 || response.status == 404)
        {
            alert("Invalid username or password");
        }
        else if(response.status == 200)
        {
            localStorage.setItem("username", username);
            localStorage.setItem("password", password);
            window.location.href = "/";
        }

    });
}



export default LoginPage;
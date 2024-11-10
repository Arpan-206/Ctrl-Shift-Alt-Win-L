import axios from "axios"
export default async function GetTimeLine()
{
    let data = null;
    let username = localStorage.getItem("username");
    let password = localStorage.getItem("password");

    if (!username || !password) {
        // redirect to login page
        window.location.href = "/login";
    }


    let response = await fetch("https://watermelon-bpwf.onrender.com/movies/", {
        method: "GET",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "text/plain",
            "Accept": "application/json",
            "Authorization": `Basic ${btoa(username + ':' + password)}`
        },
    }).then(async response => {
        data =  await response.json();
    });
    return data;
}
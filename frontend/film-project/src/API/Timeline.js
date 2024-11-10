import axios from "axios"
export default async function GetTimeLine()
{
    let data = null;
    let response = await fetch("https://watermelon-bpwf.onrender.com/movies/", {
        method: "GET",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        auth: {
            username: "abra",
            password: "abc"
        },
        withCredentials: false,
    }).then(response => {
        data =  response.data;
    });
    return data;
}
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
            "Accept": "application/json",
            "Authorization": `Basic ${btoa('abra' + ':' + 'abc')}`
        },
    }).then(async response => {
        data =  await response.json();
        console.log(data);
    });
    return data;
}
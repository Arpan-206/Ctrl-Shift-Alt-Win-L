export default async function GetDiscoveryData()
{
    let data = null;
    let response = await fetch("https://watermelon-bpwf.onrender.com/recommend_movies/", {
        method: "GET",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "text/plain",
            "Accept": "application/json",
            "Authorization": `Basic ${btoa('abra' + ':' + 'abc')}`
        },
    }).then(async response => {
        data =  await response.json();
        console.log(data);
    });
    return data;
}
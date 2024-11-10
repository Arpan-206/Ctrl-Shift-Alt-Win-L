import axios from "axios";


export default async function SubmitItems(title, dateWatched, review, rating)
{
    var request = await axios.post("https://watermelon-bpwf.onrender.com/movies/", 
        {
            "imdb_id": "", // either this or title
            "title": title, // only if no imdb_id
            "date_watched": dateWatched, // in YYYY-MM-DD
            "review": review, 
            "rating": rating, // Out of 10
          }
    );
    return request.data;
}
export async function GetItems(searchValue)
{
    var data = null;
    var request = await axios.get("https://watermelon-bpwf.onrender.com/suggest_titles/?current_param=" + searchValue,
    {
    }
    
).then(response => {
    console.log(response);
    data = response;
});
    return data;
}


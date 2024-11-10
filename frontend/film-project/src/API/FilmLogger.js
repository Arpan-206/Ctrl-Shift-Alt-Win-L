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
}
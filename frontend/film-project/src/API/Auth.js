import axios from 'axios';
export default function GetAPIToken(access_token)  
{
    var options = {
        method: 'POST',
        url: 'https://hrbt.us.auth0.com/oauth/token',
        headers: {'content-type': 'application/x-www-form-urlencoded'},
        data: new URLSearchParams({
          grant_type: 'authorization_code',
          client_id: 'zNvth0HUbVkjW3NuTVanbLy3ZpgzakSt',
          client_secret: 'lwjpJpylQpV2PHQ2mjx3wPR61opiJ4llbeWnwrXX5VPAnGwg_dXXp-G3wKXVmqRS',
          code: access_token,
          redirect_uri: 'http://localhost:5173/api/auth/callback',
        })
      };
      
      axios.request(options).then(function (response) {

        // save the access_token in local storage
        localStorage.setItem('api_token', response.data);
      }).catch(function (error) {
        console.error(error);
      });
}
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { Auth0Provider } from '@auth0/auth0-react';
import {NextUIProvider} from '@nextui-org/react'
createRoot(document.getElementById('root')).render(
  
  <Auth0Provider
    domain="hrbt.us.auth0.com"
    clientId="zNvth0HUbVkjW3NuTVanbLy3ZpgzakSt"
    authorizationParams={{
      redirect_uri: window.location.origin,
      audience: "https://hrbt.us.auth0.com/api/v2/",
      scope: "read:current_user update:current_user_metadata"
    }}
  >
    <NextUIProvider>
    <App />
    </NextUIProvider>
  </Auth0Provider>,
)

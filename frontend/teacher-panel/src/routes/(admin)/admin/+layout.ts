import { browser } from "$app/environment";
import type { LayoutLoad } from './$types';
import Keycloak, {type KeycloakInitOptions} from 'keycloak-js';
import {PUBLIC_KEYCLOAK_BASE_URL } from '$env/static/public'


export const ssr = false;
export const csr = true;

export const load: LayoutLoad = async () => {
  console.log("KC URL")
  console.log(`${PUBLIC_KEYCLOAK_BASE_URL}`)

  let instance = {
    url: `${PUBLIC_KEYCLOAK_BASE_URL}`,
    realm: 'DM885',
    clientId: 'svelte-admin'
  };

  let keycloak = new Keycloak(instance);
  let kcInitOpts: KeycloakInitOptions = { 
    onLoad: "login-required", 
    checkLoginIframe: false,
  };
  
  let keycloakPromise;
  if (browser) {
    keycloakPromise = keycloak.init(kcInitOpts).then((auth) => {
      console.log("Auth", auth)
      if (auth) {
        document.cookie= "kc-cookie=" + keycloak.token + "; path=/; SameSite=strict";
        console.log("KC token", keycloak.token)
        return keycloak;
      }
    });
  }

  return {
    keycloak: await keycloakPromise,
    //keycloak
  };
};
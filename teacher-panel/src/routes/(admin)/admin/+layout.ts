import { browser } from "$app/environment";
import type { LayoutLoad } from './$types';
import Keycloak, {type KeycloakInitOptions} from 'keycloak-js';

export const ssr = false;
export const csr = true;

export const load: LayoutLoad = async ({data}) => {
  let instance = {
    url: `http://localhost:3200/`,
    realm: 'DM885',
    clientId: 'svelte'
  };

  let keycloak = new Keycloak(instance);
  let kcInitOpts: KeycloakInitOptions = { 
    onLoad: "login-required", 
    checkLoginIframe: false,
  };
  
  let keycloakPromise;
  if (browser) {
    keycloakPromise = keycloak.init(kcInitOpts).then((auth) => {
      if (auth) {
        document.cookie= "kc-cookie=" + keycloak.token + "; path=/; SameSite=strict";
        return keycloak;
      }
    });
  }

  return {
    keycloak: keycloakPromise,
  };
};
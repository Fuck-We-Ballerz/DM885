import type { PageLoad } from './$types';
import { PUBLIC_KEYCLOAK_REDIRECT_HOME_URL } from '$env/static/public'


export const load: PageLoad = async ({parent, data}) => {
  let postLogoutUrl = PUBLIC_KEYCLOAK_REDIRECT_HOME_URL
  let parentData = await parent();
  let {keycloak} = parentData;
  return {
    keycloak: keycloak,
    postLogoutUrl: postLogoutUrl
  }
};
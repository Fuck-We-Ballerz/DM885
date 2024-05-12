
<svelte:head>
    <title>Logout</title> 
</svelte:head>

<script lang="ts">
    import { onMount } from 'svelte';
    import type {KeycloakLogoutOptions} from 'keycloak-js';
    import { PUBLIC_KEYCLOAK_REDIRECT_HOME_URL } from '$env/static/public';

    export let data;
    onMount(
        () => setTimeout(() => {
            let logoutOptions: KeycloakLogoutOptions = {
                redirectUri: `${PUBLIC_KEYCLOAK_REDIRECT_HOME_URL}`,
            };
            if (data.keycloak) {
                data.keycloak.logout(logoutOptions);
            }
        }, 2000)
    );
</script>

<p>Logging Out...</p>
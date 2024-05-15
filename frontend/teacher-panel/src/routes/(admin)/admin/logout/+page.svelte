<svelte:head>
    <title>Logout</title> 
</svelte:head>

<script lang="ts">
    import { onMount } from 'svelte';
    import type {KeycloakLogoutOptions} from 'keycloak-js';

    export let data;
    onMount(
        () => setTimeout(() => {
            let logoutOptions: KeycloakLogoutOptions = {
                redirectUri: "http://localhost:5173/",
            };
            if (data.keycloak) {
                data.keycloak.logout(logoutOptions);
            }
        }, 2000)
    );
</script>

<p>Logging Out...</p>
<script lang="ts">
    import { base } from '$app/paths';
    import type { PageData } from './$types';

    export let data: PageData;
    console.log(data);
</script>

<h1>Choose your role below</h1>

<button on:click={() => { window.location.href = `${data.studentUrl}`; }}>Student</button>
<button on:click={() => { window.location.href = `${base}/teacher`; }}>Teacher</button>
<button on:click={() => { window.location.href = `${base}/admin`; }}>Admin</button>


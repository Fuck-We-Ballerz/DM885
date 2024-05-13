<script>
    import { PUBLIC_STUDENT_LOGIN_URL } from "$env/static/public";
    import { base } from '$app/paths';

</script>

<h1>Choose your role below</h1>

<button on:click={() => { window.location.href = `${PUBLIC_STUDENT_LOGIN_URL}`; }}>Student</button>
<button on:click={() => { window.location.href = `${base}/teacher`; }}>Teacher</button>
<button on:click={() => { window.location.href = `${base}/admin`; }}>Admin</button>


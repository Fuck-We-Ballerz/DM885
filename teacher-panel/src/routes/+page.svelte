<script>
    import { PUBLIC_STUDENT_LOGIN_URL } from "$env/static/public";
</script>

<h1>Choose your role below</h1>

<button on:click={() => { window.location.href = `${PUBLIC_STUDENT_LOGIN_URL}`; }}>Student</button>
<button on:click={() => { window.location.href = '/teacher'; }}>Teacher</button>
<button on:click={() => { window.location.href = '/admin'; }}>Admin</button>


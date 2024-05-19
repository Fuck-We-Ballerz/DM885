<script>
    import cookie from 'cookie';
    // export let data;

    // function handleSubmit(event) {
    //         event.preventDefault();
    //         // Add your submit logic here
    //     }
</script>

<h1>Create Teacher</h1>

<form method="POST">   
    <label for="firstName">First Name:</label>
    <input type="text" id="firstName" name="firstName" style="display: block;">

    <label for="lastName">Last Name:</label>
    <input type="text" id="lastName" name="lastName" style="display: block;">

    <label for="username">Username:</label>
    <input type="text" id="username" name="username" style="display: block;">

    <button type="submit">Submit</button>
    <button type="reset">Reset</button>
</form>

<script lang="ts">
    import type { PageData } from './$types';
    import { base } from '$app/paths';

    export let data: PageData;
    data.teachers.sort((a, b) => a.name.localeCompare(b.name)); //List of teachers sorted by name
    data.students.sort((a, b) => a.name.localeCompare(b.name)); //List of teachers sorted by name

    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();
        const target = event.target;
        if (target instanceof HTMLFormElement) {
            const formData = new FormData(target)

            // Send form data with a POST request
            const response = await fetch(`${base}/admin/delete`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                console.log('Form data sent successfully');
                location.reload();
            } else {
                console.error('Failed to send form data');
            }
        }
    }
</script>
<h1>Teachers</h1>
<form on:submit={handleSubmit}>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>
            {#each data.teachers as teacher}
            <tr>
                <td>{teacher.name}</td>
                <td>{teacher.username}</td>
                <td><input type="checkbox" name={teacher.username} /></td>
            </tr>
            {/each}
        </tbody>
    </table>
    <button type="submit">Submit</button>
</form>

<h1>Students</h1>
<form on:submit={handleSubmit}>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Delete</th>
            </tr>
        </thead>
        <tbody>
            {#each data.students as student}
            <tr>
                <td>{student.name}</td>
                <td>{student.username}</td>
                <td><input type="checkbox" name={student.username} /></td>
            </tr>
            {/each}
        </tbody>
    </table>
    <button type="submit">Submit</button>
</form>
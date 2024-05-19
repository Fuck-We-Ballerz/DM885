<script lang="ts">
    import type { PageData } from './$types';
    import { base } from '$app/paths';

    export let data: PageData;
    data.teachers.sort((a, b) => a.name.localeCompare(b.name)); //List of teachers sorted by name


    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();
        const target = event.target;
        if (target instanceof HTMLFormElement) {
            const formData = new FormData(target);

            // Manually include checkboxes that are 'off', since a FormData object only includes checkboxes that are 'on' (no matter what)
            data.teachers.forEach(teacher => {
                if (!teacher.isPaused) {
                    formData.append(teacher.username, 'off');
                }
            })

            // Send form data with a POST request
            const response = await fetch(`${base}/admin/pause`, {
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

<form on:submit={handleSubmit}>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Paused</th>
            </tr>
        </thead>
        <tbody>
            {#each data.teachers as teacher}
            <tr>
                <td>{teacher.name}</td>
                <td>{teacher.username}</td>
                <td><input type="checkbox" name={teacher.username} bind:checked={teacher.isPaused} /></td>
            </tr>
            {/each}
        </tbody>
    </table>
    <button type="submit">Submit</button>
</form>
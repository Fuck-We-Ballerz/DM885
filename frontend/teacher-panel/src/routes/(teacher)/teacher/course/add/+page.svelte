<script lang="ts">
    import type { PageData } from './$types';
    import { base } from '$app/paths';

    export let data: PageData;
    data.students.sort((a, b) => a.name.localeCompare(b.name)); //List of students sorted by name


    async function handleSubmit(event: SubmitEvent) {
        event.preventDefault();
        const target = event.target;
        if (target instanceof HTMLFormElement) {
            const formData = new FormData(target)

            // Send form data with a POST request
            const response = await fetch(`${base}/teacher/course/add`, {
                method: 'POST',
                body: formData
            });
        }
    }
</script>

<h1>Add Students To A Course</h1>
<form on:submit={handleSubmit}>
    <label>
        Course
        <select id="course" name="course">
            {#each data.courses as course, i}
                <option value="{course.id}">{course.name}</option>
            {/each}
        </select>
    </label>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Username</th>
                <th>Add</th>
            </tr>
        </thead>
        <tbody>
            {#each data.students as student}
            <tr>
                <td>{student.name}</td>
                <td>{student.username}</td>
                <td><input type="checkbox" name={student.username} value="{student.id}" /></td>
            </tr>
            {/each}
        </tbody>
    </table>
    <button type="submit">Submit</button>
</form>
<script lang="ts">
    import type { PageData } from './$types';
    import { base } from '$app/paths';

    export let data: PageData;
    data.students.sort((a, b) => a.name.localeCompare(b.name)); //List of students sorted by name


    // async function handleSubmit(event: SubmitEvent) {
    //     event.preventDefault();
    //     const target = event.target;
    //     if (target instanceof HTMLFormElement) {
    //         const formData = new FormData(target)

    //         // Send form data with a POST request
    //         const response = await fetch(`${base}/teacher/assignment/add`, {
    //             method: 'POST',
    //             body: formData
    //         });

    //         if (response.ok) {
    //             console.log('Form data sent successfully');
    //             location.reload();
    //         } else {
    //             console.error('Failed to send form data');
    //         }
    //     }
    // }
</script>

<h1>Add Students To An Assignment</h1>
<form method="post">
    <label>
        Assignment
        <select id="assignment" name="assignment">
            {#each data.assignments as assignment, i}
                <option value="{assignment.id}">{assignment.title}</option>
            {/each}
        </select>
    </label>
    <div style="margin-top: 20px;">Enrolled Students in {data.courseName}</div>
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
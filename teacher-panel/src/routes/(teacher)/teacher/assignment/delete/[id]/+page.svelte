<script lang="ts">
    import type { PageData } from './$types';
    import { base } from '$app/paths';

    export let data: PageData;
    data.students.sort((a, b) => a.name.localeCompare(b.name)); //List of students sorted by name
</script>

<h1>Remove Students from Assignment {data.assignmentName} </h1>
<form method="post">
    <div style="margin-top: 20px;">Students currently added to {data.assignmentName}</div>
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
            <td><input type="hidden" name="assignmentId" value="{data.assignmentId}" /></td>
        </tbody>
    </table>
    <button type="submit">Remove From Assignment</button>
</form>
<script lang="ts">
    import type { PageData } from './$types';
    import { base } from '$app/paths';
    import { student } from '$lib/db/schema';

    export let data: PageData;
    data.students.sort((a, b) => a.name.localeCompare(b.name)); //List of students sorted by name
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
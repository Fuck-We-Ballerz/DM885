<script lang="ts">
    import type { PageData } from './$types'
    import { base } from '$app/paths'

    export let data: PageData
    let selectedAssignment = data.assignments[0]?.id
</script>

<h1>Remove Students From An Assignment</h1>
<form>
    <label>
        Assignment
        <select id="course" name="course" bind:value={selectedAssignment}>
            {#each data.assignments as assignment, i}
                <option value="{assignment.id}">{assignment.title}</option>
            {/each}
        </select>
    </label>
    <button on:click={() => { window.location.href = `${base}/teacher/assignment/delete/${selectedAssignment}`; }}>Remove Student From Assignment</button>
</form>
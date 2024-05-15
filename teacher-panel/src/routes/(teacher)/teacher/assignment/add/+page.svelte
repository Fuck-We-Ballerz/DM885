<script lang="ts">
    import type { PageData } from './$types'
    import { base } from '$app/paths'

    export let data: PageData
    let selectedCourse = data.courses[0]?.id
</script>

<h1>Add Students To An Assignment</h1>
<form>
    <label>
        Course
        <select id="course" name="course" bind:value={selectedCourse}>
            {#each data.courses as course, i}
                <option value="{course.id}">{course.name}</option>
            {/each}
        </select>
    </label>
    <button on:click={() => { window.location.href = `${base}/teacher/assignment/add/${selectedCourse}`; }}>Add Students</button>
</form>
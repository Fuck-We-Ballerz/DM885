<script lang="ts">
	import type { PageData } from './$types'
    import { base } from '$app/paths'
	
	export let data: PageData;
    
    data.students.sort((a, b) => a.name.localeCompare(b.name));
</script>

<h1>Students in {data.assignment.title}</h1>

{#each data.students as student, i}
<table>
    <tr>
        <td>
            <h2>Student: {student.name}</h2>
            <div style="display: flex; justify-content: space-between;">
                <button on:click={() => window.location.href = `${base}/teacher/submission/${data.assignment.id}/${student.id}`}>
                    Check Submissions
                </button>
                <button>Extract logs in Zip file</button>
                <button>Extract metadata in CSV </button>
            </div>
        </td>
    </tr>
</table>
{/each}




<style>
    /* Add a border to the table */
    /* Add spacing between the tables */
    table {
        border: 1px solid black;
        margin: 10px;
    }
</style>
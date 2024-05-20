<script lang="ts">
	import type { PageData } from './$types'
    import { base } from '$app/paths'
	
	export let data: PageData;
    
    data.assignments.sort((a, b) => a.title.localeCompare(b.title));
</script>

<h1>Assignments</h1>

{#each data.assignments as assignment, i}
<table>
    <tr>
        <td>
            <h2>{assignment.title}</h2>
            <div style="display: flex; justify-content: space-between;">
                <button on:click={() => window.location.href = `${base}/teacher/submission/${assignment.assignmentId}`}>
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
<script lang="ts">
	import type { PageData } from './$types'
    import { base } from '$app/paths'
    import { onMount} from 'svelte';
    import { getZIP, getCSV } from '$lib/utils';
	
	export let data: PageData;
    
    data.students.sort((a, b) => a.name.localeCompare(b.name));

    onMount(() => {
        if (data && data.submissionsCSV && data.submissionsCSV.length > 0 && data.submissionsZIP && data.submissionsZIP.length > 0) {
            
            getCSV(data.submissionsCSV, false);
            getZIP(data.submissionsZIP, false);

        }
    });
</script>

<h1>Students in {data.assignment.title}</h1>
<button id="csv">Extract CSV Metadata</button>
<button id="zip">Extract Zip Logs</button>

{#each data.students as student, i}
<table>
    <tr>
        <td>
            <h2>Student: {student.name}</h2>
            <div style="display: flex; justify-content: space-between;">
                <button on:click={() => window.location.href = `${base}/teacher/submission/${data.assignment.id}/${student.id}`}>
                    Check Submissions
                </button>
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
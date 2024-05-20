<script lang="ts">
	import { submission } from '$lib/db/schema';
import type { PageData } from './$types';
	export let data: PageData;

</script>

<h1>Submissions for {data.studentName}</h1>

{#each data.submissions as submission, i}

<table>
    <tr>
        <td>
            <div style="display: flex; justify-content: space-between;">
                <h2>{submission.id}</h2>
            </div>
            <div>
                <table>
                    <tr>
                        <td>Submission ID: {submission.id}</td>
                    </tr>
                    <tr>
                        <td>Grade</td>
                        <td style="color: {submission.grade === 'failed' ? 'red' : submission.grade === 'passed' ? 'green' : 'black'};">{submission.grade}</td>
                    </tr>
                    <tr>
                        <td>Status</td>
                        <td>{submission.status}</td>
                    </tr>
                    <tr>
                        <td>std</td>
                        <td>{submission.submission_std}</td>
                    </tr>
                    <tr>
                        <td>err</td>
                        <td>{submission.submission_err}</td>
                    </tr>
                    <tr>
                        <td>Submission time</td>
                        <td>{submission.submission_time}</td>
                    </tr>
                </table>
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
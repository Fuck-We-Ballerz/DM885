<script lang="ts">
	import type { PageData } from './$types';
	
	export let data: PageData;
    console.log("From client")
    console.log(data)

    data.assignments.sort((a, b) => a.title.localeCompare(b.title));

    let isEditing: number | null = null;

    let formAction = '';

    function setFormAction(action: string) {
        formAction = action;
    }
</script>

<h1>Assignments</h1>

{#each data.assignments as assignment, i}

<table>
    <tr>
        <td>
            <div style="display: flex; justify-content: space-between;">
                <h2>{assignment.title}</h2>
                {#if isEditing === i}
                    <button on:click={() => isEditing = isEditing === i ? null : i} style="height: 30px;">Cancel</button>
                {:else}
                    <button on:click={() => isEditing = isEditing === i ? null : i} style="height: 30px;">Edit</button>
                {/if}
            </div>
            <div>
                <form method="POST" action={formAction}>
                    <table>
                        <tr>
                            <td>Course: {assignment.courseName}, id: {assignment.course}</td>
                            {#if isEditing === i}
                                <input type="hidden" name="assignmentId" value={assignment.assignmentId} />
                            {/if}
                        </tr>
                        <tr>
                            <td>Configuration</td>
                            {#if isEditing === i}
                                <tr>
                                    <td>Config: {assignment.config}</td>
                                </tr>
                                <tr>
                                    <select id="assignmentConfig" name="assignmentConfig" value={assignment.config}>
                                        {#each data.assignmentConfigs as { id }, i}
                                            <option value="{id}">Config{id}</option>
                                        {/each}
                                    </select>
                                </tr>
                            {:else}
                                <td>Config: {assignment.config}</td>
                            {/if}
                        </tr>
                        <tr>
                            <td>Starting Date</td>
                            {#if isEditing === i}
                            <tr>
                                <td>Old Date: {assignment.startDate}</td>
                            </tr>
                            <tr>
                                <td><input type="date" name="startDate" value={assignment.startDate} /></td>
                            </tr>
                            {:else}
                                <td>{assignment.startDate}</td>
                            {/if}
                        </tr>
                        <tr>
                            <td>Submission Due</td>
                            {#if isEditing === i}
                            <tr>
                                <td>Old Date: {assignment.endDate}</td>
                            </tr>
                            <tr>
                                <td><input type="date" name="endDate" value={assignment.endDate} /></td>
                            </tr>
                            {:else}
                                <td>{assignment.endDate}</td>
                            {/if}
                        </tr>
                        <tr>
                            <td>Docker Image</td>
                            {#if isEditing === i}
                                <td><input type="text" name="dockerImage" value={assignment.dockerImage} /></td>
                            {:else}
                                <td>{assignment.dockerImage}</td>
                            {/if}
                        </tr>
                        <tr>
                            <td>Visible for students</td>
                            {#if isEditing === i}
                                <select name="isVisible" value={assignment.isVisible.toString()}>
                                    <option value="true">true</option>
                                    <option value="false">false</option>
                                </select>

                                <!-- <td><input type="text" name="isVisible" value={assignment.isVisible} /></td> -->
                            {:else}
                                <td>{assignment.isVisible}</td>
                            {/if}
                        </tr>
                    </table>
                    {#if isEditing === i}
                        <div style="display: flex; justify-content: space-between;">
                            <button type="submit" on:click={() => setFormAction('?/updateAssignment')}>Submit</button>
                            <button type="submit" on:click={() => setFormAction('?/deleteAssignment')}>Delete</button>
                        </div>
                    {/if}
                </form>
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
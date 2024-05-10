<script lang="ts">
	import type { PageData } from './$types';
	
	export let data: PageData;
</script>

<div style="display: flex;">
    <!-- This is the create configuration -->
    <div style="flex: 1;">
        <div style="display: flex; flex-direction: row; align-items: center;">
            <h2 style="margin-right: 10px;">Assignment Configurations</h2>
            <div style="border-left: 1px solid black; height: 100%; margin-right: 10px;"></div>
            <form method="POST" action="?/newConfig">
                <button style="background-color: green; padding: 10px;">Add Configuration</button>
            </form>    
        </div>

        <div style="overflow-y: scroll; max-height: 400px;">
            {#each data.assignmentConfigs2 as configuration, i}
                <table>
                    <tr>
                        <td>
                            <div style="display: flex; flex-direction: row;">
                                <h2>Config {configuration.id}</h2>
                            
                                <form method="POST" action="?/deleteConfig">
                                    <input type="hidden" name="id" value="{configuration.id}">
                                    <button style="background-color: red; padding: 5px;">Delete</button>
                                </form>
                                <form method="POST" action="?/editConfig">
                                    <input type="hidden" name="id" value="{configuration.id}">
                                    <button style="background-color: blue; padding: 5px;">Edit</button>
                                </form>
                            </div>

                            <div>
                                <table>
                                    <tr>
                                        <td>Max CPU</td>
                                        <td>{configuration.max_cpu}</td>
                                    </tr>
                                    <tr>
                                        <td>Max RAM</td>
                                        <td>{configuration.max_ram}</td>
                                    </tr>
                                    <tr>
                                        <td>Max Submissions</td>
                                        <td>{configuration.max_submission}</td>
                                    </tr>
                                    <tr>
                                        <td>Max Time</td>
                                        <td>{configuration.max_time}</td>
                                    </tr>
                                </table>
                            </div>
                        </td>
                    </tr>
                </table>
            {/each}
        </div>
    </div>

    <!-- This is the create assignment -->
    <div style="flex: 3;">
        <form method="POST" action="?/newAssignment">
            <h2>Create an Assignment</h2>
            <label>
                Title
                <input type="text" id="title" name="title" required>
            </label>
            <label>
                Docker Image
                <textarea id="docker-image" name="docker-image" required></textarea>
            </label>
            <label>
                Start Date
                <input type="date" id="startDate" name="startDate" required>
            </label>
            <label>
                Due Date
                <input type="date" id="dueDate" name="dueDate" required>
            </label>
            <label>
                Assignment Configuration
                <select id="assignmentConfig" name="assignmentConfig">
                    {#each data.assignmentConfigs2 as { id }, i}
                        <option value="{id}">Config{id}</option>
                    {/each}
                </select>
            </label>
            <div style="display: flex; justify-content: center;">
                <button type="submit">Create</button>
                <button type="reset">Reset</button>
            </div>
        </form>
    </div>
</div>

<style>
    /* Center the form */
    form {
        display: flex;
        flex-direction: column;
        align-items: center;
        
    }
    /* Make description have a max width */
    textarea {
        max-width: 100%;
    }
</style>
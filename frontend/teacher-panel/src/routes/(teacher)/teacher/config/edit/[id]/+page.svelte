<script lang="ts">
  import type { PageData } from './$types';
  import { base } from '$app/paths';

  export let data: PageData;
</script>

<h1>Edit Config</h1>
<p>Configuration: {data.data.id}</p>
<form method="POST" action="?">
  <table>
    <tr>
      <td>
        <div>
          <table>
            <tr>
              <td>Max CPU</td>
              <td><input type="number" name="max_cpu" bind:value={data.data.max_cpu} /></td>
              <td>vCPU</td>
            </tr>
            <tr>
              <td>Max RAM</td>
              <td><input type="number" name="max_ram" bind:value={data.data.max_ram} /></td>
              <td>MegaBytes</td>
            </tr>
            <tr>
              <td>Max Submissions</td>
              <td><input type="number" name="max_submission" bind:value={data.data.max_submission} /></td>
            </tr>
            <tr>
              <td>Max Time</td>
              <td><input type="number" name="max_time" value={data.data.max_time}/></td>
              <td>seconds</td>
            </tr>
          </table>
        </div>
      </td>
    </tr>
  </table>
  <button type="submit">Save</button>
</form>
  
<button on:click={() => { window.location.href = `${base}/teacher/assignment/create`; }}>Back to assignments</button>


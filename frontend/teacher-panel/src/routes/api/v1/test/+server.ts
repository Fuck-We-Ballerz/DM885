import { zipSubmissions } from '$lib/api/utilities.js';
export const GET = async () => {
    // This endpoint returns a sample zip file containing 4 submissions.
    // It is meant to be used for testing purposes.
    const subs = [];

    for (let i = 0; i < 4; i++) {
        const sub = {
            student_id: i,
            stdout: "This is some text from stdout" + i,
            stderr: "Errlog for submission " + i,
        };
        subs.push(sub);
    }
    const blob = await zipSubmissions(subs);
    
    return new Response(await blob.arrayBuffer(), { 
        status: 200, 
        headers: {
            'Content-Type': 'application/zip',
            'Content-Disposition': 'attachment; filename="submissions.zip"',
        }
    });
};
import { db } from '$lib'
import{ eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import JSZip from 'jszip';


/**
 * Returns a zip file containing the logs for each student for a given assignment
 */
export const GET = async ({params, request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const assignment_id: number = parseInt(params.assignment_id);
    
    const submissions = await db.select({
        student_id: schema.submission.student_id,
        stdout: schema.submission.submission_std,
        stderr: schema.submission.submission_err
    }).from(schema.submission)
      .where(eq(schema.submission.assignment_id, assignment_id));

    const zip = new JSZip();

    for (let i = 0; i < submissions.length; i += 1) {
        const submission = submissions[i];
        const student_folder = zip.folder(`student_${submission.student_id}`);
        if (!student_folder) {
            return new Response(JSON.stringify({
                message: `Failed to create folder for student ${submission.student_id}`
            }), { status: 500 });
        }
        student_folder.file("stdout.txt", submission.stdout);
        student_folder.file("stderr.txt", submission.stderr);
    }

    const zipFile = await zip.generateAsync({ type: "blob" });

    return new Response(JSON.stringify({
        message: "Success",
        zipFile: zipFile
    }), { status: 200 });
};
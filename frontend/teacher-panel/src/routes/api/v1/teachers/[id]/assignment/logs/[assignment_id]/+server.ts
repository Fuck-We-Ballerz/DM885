import { db } from '$lib'
import{ eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import JSZip from 'jszip';
import { login } from '$lib/api/login';
import { zipSubmissions } from '$lib/api/utilities';


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

    const zipFile = await zipSubmissions(submissions);
    
    return new Response(JSON.stringify({
        message: "Success",
        zipFile: zipFile
    }), { status: 200 });
};
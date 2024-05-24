import { db } from '$lib'
import{ and, eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import JSZip from 'jszip';
import { login } from '$lib/api/login';
import { zipSubmissions } from '$lib/api/utilities';

/**
 * Returns a zip file containing the logs for the given student for a given assignment
 */
export const GET = async ({request}) => {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    const data = await request.json();

    const assignment_id: number = data.assignment_id;
    const student_id: number = data.student_id;
    
    const submissions = await db.select({
        student_id: schema.submission.student_id,
        stdout: schema.submission.submission_std,
        stderr: schema.submission.submission_err
    }).from(schema.submission)
      .where(and(
            eq(schema.submission.assignment_id, assignment_id),
            eq(schema.submission.student_id, student_id)
        ));

    const zipFile = await zipSubmissions(submissions);

    return new Response(JSON.stringify({
        message: "Success",
        zipFile: zipFile
    }), { status: 200 });
};
import { db } from '$lib'
import{ and, eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';


/**
 * Returns a csv file containing the metadata for a given student for a given assignment
 */
export const GET = async ({request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const data = await request.json();
    const assignment_id = data.assignment_id;
    const submissions = await db.select().from(schema.submission)
      .where(and(
            eq(schema.submission.assignment_id, assignment_id),
            eq(schema.submission.student_id, data.student_id))
        );

    const csv_header = "student_id,submission_id,status,grade,submission_std,submission_err\n"

    const csv_body = submissions.map((submission) => {
        return `${submission.student_id},${submission.id},${submission.status},${submission.grade},${submission.submission_std},${submission.submission_err}\n`
    }).join('')

    const csv = csv_header + csv_body;    

    return new Response(JSON.stringify({
        message: "Success",
        csv: csv
    }), { status: 200 });
};
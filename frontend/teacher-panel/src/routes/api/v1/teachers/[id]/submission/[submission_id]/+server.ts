import { db } from '$lib'
import{ eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

/**
 * Returns the status, output and the result of the given submission
 */
export const GET = async ({request, params}) => {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    const submission_id: number = parseInt(params.submission_id);

    const submissions = await db.select({
        status: schema.submission.status,
        stdout: schema.submission.submission_std,
        stderr: schema.submission.submission_err,
        result: schema.submission.grade
    }).from(schema.submission)
      .where(eq(schema.submission.id, submission_id));
                                

    return new Response(JSON.stringify({
        message: "Success",
        submissions: submissions
    }), { status: 200 });
};
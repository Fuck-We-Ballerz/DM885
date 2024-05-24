import { db } from '$lib'
import{ eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

/**
 * Cancel the evaluation of all submissions for an assignment.
 */
export const POST = async ({params, request}) => {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    const assignment_id: number = parseInt(params.assignment_id);
    
    const new_status = "cancelled"

    const [success] = await db.update(schema.submission).set({
        status: new_status,
    }).where(eq(schema.submission.assignment_id, assignment_id)).returning();

    if (!success) {
        return new Response(JSON.stringify({
            message: "Failed to cancel the submissions"
        }), { status: 500 });
    }

    return new Response(JSON.stringify({
        message: "Success",
    }), { status: 200 });
};
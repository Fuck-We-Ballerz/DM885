import { db } from '$lib'
import{ eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

/**
 * Set the status of a submission
 */
export const POST = async ({params, request}) => {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    const data = await request.json();
    const submission_id: number = parseInt(params.submission_id);
    const new_status = data.status;

    switch (new_status) {
        case "pending":
            break;
        case "running":
            break;
        case "completed":
            break;
        case "failed":
            break;
        case "cancelled":
            break;
        default:
            return new Response(JSON.stringify({
                message: "Invalid status"
            }), { status: 400 });
    }

    const [success] = await db.update(schema.submission).set({
        status: new_status,
    }).where(eq(schema.submission.id, submission_id)).returning();

    if (!success) {
        return new Response(JSON.stringify({
            message: "Failed to reevaluate the submission"
        }), { status: 500 });
    }

    return new Response(JSON.stringify({
        message: "Success",
    }), { status: 200 });
};
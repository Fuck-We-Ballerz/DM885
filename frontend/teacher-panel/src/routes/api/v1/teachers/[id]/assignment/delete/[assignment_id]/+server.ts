import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login'

/**
 * Deletes an assignment and unassigns the teachers and students that were assigned to that assignment.
 */
export const DELETE = async ({params, request}) => {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    const assignment_id = parseInt(params.assignment_id);

    await db.delete(schema.teacher_to_assignment)
        .where(eq(schema.teacher_to_assignment.assignment_id, assignment_id));

    await db.delete(schema.student_to_assignment)
        .where(eq(schema.student_to_assignment.assignment_id, assignment_id));

    await db.delete(schema.submission)
        .where(eq(schema.submission.assignment_id, assignment_id));

    const [result] = await db.delete(schema.assignment)
                            .where(eq(schema.assignment.id, assignment_id))
                            .returning();


    return new Response(JSON.stringify({
        message: "Success", 
        deleted_assignament: result
    }), { status: 200 } );
}

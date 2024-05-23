import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login'

/**
 * Enroll a student into the given assignment
 */
export const POST = async ({params, request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const studentId = parseInt(params.student_id);
    const data = await request.json();

    const [success] = await db.insert(schema.student_to_assignment).values({
        assignment_id: data.assignment_id,
        student_id: studentId 
    }).returning();

    if (!success) {
        return new Response(JSON.stringify({
            message: "Failed to insert student_to_assignment"
        }), { status: 500 });
    }

    return new Response(JSON.stringify({
        message: "Success"
    }), { status: 201 } );
}

/**
 * Unenroll a student into the given assignment
 */
export const DELETE = async ({params, request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const studentId = parseInt(params.student_id);
    const data = await request.json();

    const [success] = await db.delete(schema.student_to_assignment)
        .where(eq(schema.student_to_assignment.student_id, studentId))
        .returning();

    if (!success) {
        return new Response(JSON.stringify({
            message: `Failed to unenroll the student with id: ${studentId}`
        }), { status: 500 });
    }

    return new Response(JSON.stringify({
        message: "Success"
    }), { status: 201 } );
}

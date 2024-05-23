import { db } from '$lib'
import{ eq, inArray } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

/**
 * Enroll a list of student into the given assignment
 */
export const POST = async ({params, request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const data = await request.json();
    const ids: [number] = data.student_ids;

    const studentIds: {assignment_id: number, student_id: number}[] = ids.map((studentId: number) => {
        return {
            assignment_id: data.assignment_id,
            student_id: studentId
        }
    });

    const [success] = await db.insert(schema.student_to_assignment).values(studentIds).returning();

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
    const data = await request.json();
    const studentIds: number[] = data.student_ids;

    const [success] = await db.delete(schema.student_to_assignment)
        .where(inArray(schema.student_to_assignment.student_id, studentIds))
        .returning();

    if (!success) {
        return new Response(JSON.stringify({
            message: `Failed to unenroll the students`
        }), { status: 500 });
    }

    return new Response(JSON.stringify({
        message: "Success"
    }), { status: 201 } );
}

/**
 * Returns all the submissions made by a student for a given assignment
 */
export const GET = async ({request}) => {
    const authorized = await login({request});
    if (authorized.status !== 200) {
        return authorized;
    }
    const data = await request.json();

    const studentId: number = data.student_id;
    const assignmentId: number = data.assignment_id;
    
    const student_submissions = await db.select()
                                .from(schema.submission)
                                .where(eq(schema.submission.student_id, studentId))
                                .as('sq');
    const submissions = await db.select()
                                .from(student_submissions)
                                .where(eq(schema.submission.assignment_id, assignmentId));

    return new Response(JSON.stringify({
        message: "Success",
        submissions: submissions
    }), { status: 200 });
};
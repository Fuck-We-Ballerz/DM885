import { eq } from 'drizzle-orm';
import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib';

export const load: PageServerLoad = async ({params}) => {   
    const assignment = await db.query.assignment.findFirst({ where: eq(schema.assignment.id, parseInt(params.id))})

    //Get all students for the assignment
    const students = await db.select().from(schema.student)
                            .innerJoin(schema.student_to_assignment, eq(schema.student.id, schema.student_to_assignment.student_id))
                            .where(eq(schema.student_to_assignment.assignment_id, assignment!.id))

    const studentList = await Promise.all(students.map(async (student) => {

        return {
            id: student.student.id,
            name: student.student.name,
            username: student.student.username
        }
    }))

    return{
        students: studentList,
        assignment: assignment!
    }
};

import { db } from '$lib'
import * as schema from '$lib/db/schema'
import type { Actions } from './$types'
import { and,eq } from 'drizzle-orm'

export async function load({cookies, params}) {
        const assignmentId = parseInt(params.id)
        const assignment = await db.query.assignment.findFirst({ where: eq(schema.assignment.id, assignmentId)})

        //Get all students for the assignment
        const students = await db.select().from(schema.student)
                    .innerJoin(schema.student_to_assignment, eq(schema.student.id, schema.student_to_assignment.student_id))
                    .where(eq(schema.student_to_assignment.assignment_id, assignmentId))
        
        let studentOutput = students.map((student) => {
            return {    
            name: student.student.name,
            id: student.student.id,
            username: student.student.username
            }
        })

        return {
            students: studentOutput,
            assignmentName: assignment!.title,
            assignmentId: assignmentId
        }
}


export const actions = {
    default: async ({cookies, request}) => {
        const data = await request.formData();
        const assignmentId = parseInt(data.get('assignmentId')!.toString())
                
        for (const [key, value] of data.entries()) {
            if (key === 'assignmentId') continue;  // Skip the entry if the key is 'assignmentId'

            const student_id = parseInt(value.toString())

            console.log("Delete student from assignment")
            await db.delete(schema.student_to_assignment).where(
                and(
                    eq(schema.student_to_assignment.student_id, student_id),
                    eq(schema.student_to_assignment.assignment_id, assignmentId)
                )
            )
        }
    }
} as Actions;
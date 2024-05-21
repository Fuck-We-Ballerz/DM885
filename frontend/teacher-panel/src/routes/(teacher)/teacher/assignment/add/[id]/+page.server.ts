import { db } from '$lib'
import * as schema from '$lib/db/schema'
import type { Actions } from './$types'
import { and,eq } from 'drizzle-orm'

export async function load({cookies, params}) {
        const courseId = parseInt(params.id)
        const course = await db.query.course.findFirst({ where: eq(schema.course.id, courseId)})

        //Get all students in the course
        const students = await db.select().from(schema.student)
                    .innerJoin(schema.student_to_course, eq(schema.student.id, schema.student_to_course.student_id))
                    .where(eq(schema.student_to_course.course_id, courseId))
        
        let studentOutput = students.map((student) => {
            return {    
            name: student.student.name,
            id: student.student.id,
            username: student.student.username
            }
        })

        //Get logged in teacher
        const teacherUsername = cookies.get('kc-username')!
        const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})
        
        //Get all assignments for the course that the teacher is teaching
        const assignments = await db.select().from(schema.assignment)
                                    .innerJoin(schema.teacher_to_assignment, eq(schema.assignment.id, schema.teacher_to_assignment.assignment_id))
                                    .where(
                                        and(
                                            eq(schema.teacher_to_assignment.teacher_id, teacher!.id),
                                            eq(schema.assignment.course_id, courseId)
                                        )
                                    )

        return {
            students: studentOutput,
            assignments: assignments.map(assigmentObj => assigmentObj.assignment),
            courseName: course!.name
        }
}


export const actions = {
    default: async ({cookies, request}) => {
        const data = await request.formData();
        
        // Retrieve the assigment
        const assignment = data.get('assignment')
        const assignmentId = parseInt(assignment!.toString())

        // Retrieve a list of student IDs from the formData
        const studentIds = Array.from(data.values())
            .slice(1)
            .filter(value => value);
        
        // Array of form [{student_id: <student_id>, assignment_id: <assignment_id>}, {student_id: <student_id>, assignment_id: <assignment_id>}, ...]}]
        const insertStudents = studentIds.map(studentId => ({
            student_id: parseInt(studentId.toString()),
            assignment_id: assignmentId
        }))

        //insert all students into the student_to_assignment table
        await db.insert(schema.student_to_assignment).values(insertStudents)
    }
} as Actions;
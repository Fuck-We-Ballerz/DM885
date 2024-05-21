import { db } from '$lib'
import * as schema from '$lib/db/schema'
import type { Actions } from './$types'
import { eq } from 'drizzle-orm'

export async function load({cookies}) {
        const students = await db.query.student.findMany() ?? []

        let studentOutput = students.map((student) => {
            return {
                name: student.name,
                id: student.id,
                username: student.username
            }
        })

        const teacherUsername = cookies.get('kc-username')!
        const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})
        
        //Get all courses that the teacher is teaching
        const courses = await db.select().from(schema.course)
                                .innerJoin(schema.teacher_to_course, eq(schema.course.id, schema.teacher_to_course.course_id))
                                .where(eq(schema.teacher_to_course.teacher_id, teacher!.id));

        return {
            students: studentOutput,
            courses: courses.map(courseObj => courseObj.course)
        }
}


export const actions = {
    default: async ({cookies, request}) => {
        const data = await request.formData();
        
        // Retrieve the course
        const course = data.get('course')
        const courseId = parseInt(course!.toString())

        // Retrieve a list of student IDs, TODO: FIx filterig out students where studnet id == course id
        const studentIds = Array.from(data.values())
            .slice(1)
            .filter(value => value);
        
        
        // Array of form [{student_id: <student_id>, course_id: <course_id>}, {student_id: <student_id>, course_id: <course_id>},, ...]}]
        const insertStudents = studentIds.map(studentId => ({
            student_id: parseInt(studentId.toString()),
            course_id: courseId
        }))

        //insert all students into the student_to_course table
        await db.insert(schema.student_to_course).values(insertStudents)
    }
} as Actions;
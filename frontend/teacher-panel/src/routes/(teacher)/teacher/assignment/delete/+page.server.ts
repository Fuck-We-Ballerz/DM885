import { db } from '$lib'
import * as schema from '$lib/db/schema'
import type { Actions } from './$types'
import { eq } from 'drizzle-orm'

export async function load({cookies}) {
    //Get logged in teacher
    const teacherUsername = cookies.get('kc-username')!
    const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})
    
    const assignments = await db.select().from(schema.assignment)
                    .innerJoin(schema.teacher_to_assignment, eq(schema.assignment.id, schema.teacher_to_assignment.assignment_id))
                    .where(eq(schema.teacher_to_assignment.teacher_id, teacher!.id))
    
    let output = await Promise.all(assignments.map(async (asg) => {
        const courseName = await db.query.course.findFirst({ where: eq(schema.course.id, asg.assignment.course_id)})

        return {
            id: asg.assignment.id,
            title: asg.assignment.title,
            assignmentId: asg.assignment.id,
            course: asg.assignment.course_id,
            courseName: courseName!.name,
            dockerImage: asg.assignment.docker_image,
            config: asg.assignment.config_id,
            isVisible: asg.assignment.is_visible,
            startDate: asg.assignment.start_date,
            endDate: asg.assignment.end_date
        }
    }))

    return {
        assignments: output
	};
}

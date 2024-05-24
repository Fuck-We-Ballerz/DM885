import { eq } from 'drizzle-orm';
import * as schema from '$lib/db/schema'
import type { PageServerLoad } from './$types';
import { db } from '$lib';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({cookies, params}) => {   
    const teacherUsername = cookies.get('kc-username')!
    const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})

    if(!teacher){
        error(403, "Access denied: user is not a teacher")
    }

    let output = []
    //Get all assignments that a teacher has
    const res = await db.select().from(schema.assignment)
                        .innerJoin(schema.teacher_to_assignment, eq(schema.assignment.id, schema.teacher_to_assignment.assignment_id))
                        .where(eq(schema.teacher_to_assignment.teacher_id, teacher!.id))
    
    output = await Promise.all(res.map(async (ass) => {
        const courseName = await db.query.course.findFirst({ where: eq(schema.course.id, ass.assignment.course_id)})

        return {
            title: ass.assignment.title,
            assignmentId: ass.assignment.id,
            course: ass.assignment.course_id,
            courseName: courseName!.name,
            dockerImage: ass.assignment.docker_image,
            config: ass.assignment.config_id,
            isVisible: ass.assignment.is_visible,
            startDate: ass.assignment.start_date,
            endDate: ass.assignment.end_date
        }
    }))

    return {
        assignments: output
    };
};

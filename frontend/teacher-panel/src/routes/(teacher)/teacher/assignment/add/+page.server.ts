import { db } from '$lib'
import * as schema from '$lib/db/schema'
import { eq } from 'drizzle-orm'
import { error } from '@sveltejs/kit';

export async function load({cookies}) {
        //Get logged in teacher
        const teacherUsername = cookies.get('kc-username')!
        const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})

        if(!teacher){
            error(403, "Access denied: user is not a teacher")
        }

            
        //Get all courses that the teacher is teaching
        const courses = await db.select().from(schema.course)
                                .innerJoin(schema.teacher_to_course, eq(schema.course.id, schema.teacher_to_course.course_id))
                                .where(eq(schema.teacher_to_course.teacher_id, teacher!.id));

        return {
            courses: courses.map(courseObj => courseObj.course),
        }
}
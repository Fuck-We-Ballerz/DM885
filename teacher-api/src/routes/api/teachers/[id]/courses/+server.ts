import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

export async function GET({params}) {
    console.log(params)

    const teacherId = parseInt(params.id)
    
    //get all courses for a teacher
    const courses = await db.select({id: schema.course.id, name: schema.course.name}).from(schema.course)
                                .innerJoin(schema.teacher_to_course, eq(schema.course.id, schema.teacher_to_course.course_id))
                                .where(eq(schema.teacher_to_course.teacher_id, teacherId));
    
    console.log(courses)
    
	return json(courses);
}
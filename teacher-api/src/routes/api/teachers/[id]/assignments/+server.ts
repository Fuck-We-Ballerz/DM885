import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'

export async function GET({params}) {
    console.log(params)

    const teacherId = parseInt(params.id)
    
    //get all assignments for a teacher
    const assignments = await db.select({
                                        id: schema.assignment.id, title: schema.assignment.title, start_date: schema.assignment.start_date, end_date: schema.assignment.end_date, 
                                        docker_image: schema.assignment.docker_image, config_id: schema.assignment.config_id, course_id: schema.assignment.course_id, is_visible: schema.assignment.is_visible
                                        })
                                .from(schema.assignment)
                                .innerJoin(schema.teacher_to_assignment, eq(schema.assignment.id, schema.teacher_to_assignment.assignment_id))
                                .where(eq(schema.teacher_to_assignment.teacher_id, teacherId));
    
    console.log(assignments)
    
	return json(assignments);
}
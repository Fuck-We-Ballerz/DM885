import { json } from '@sveltejs/kit'
import { db } from '$lib'
import{ eq } from 'drizzle-orm'
import * as schema from '$lib/db/schema'
import { login } from '$lib/api/login';

export async function GET({params, request}) {
    const authHeader = request.headers.get('Authorization');

    const authorized = await login({ authHeader: authHeader });
    if (authorized.status !== 200) {
        return authorized;
    }
    console.log(params)

    const courseId = parseInt(params.id)
    
    const students = await db.select({id: schema.student.id, name: schema.student.name, username: schema.student.username}).from(schema.student)
                    .innerJoin(schema.student_to_course, eq(schema.student.id, schema.student_to_course.student_id))
                    .where(eq(schema.student_to_course.course_id, courseId))
    
    console.log(students)
    
	return json(students);
}
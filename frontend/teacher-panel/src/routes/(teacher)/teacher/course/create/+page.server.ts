import { db} from '$lib';
import { eq } from 'drizzle-orm';
import * as schema from '$lib/db/schema'
import type { Actions } from './$types';

export const actions = {
    default: async ({cookies, request}) => {
        try {
            const teacherUsername = cookies.get('kc-username')!
            console.log(teacherUsername)
            const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})
            console.log(teacher)

            const data = await request.formData();

            const insertedCouse = await db.insert(schema.course).values({
                name: data.get('courseName')!.toString(),
            }).returning()

            const courseId = insertedCouse[0].id

            await db.insert(schema.teacher_to_course).values({
                teacher_id: teacher!.id,
                course_id: courseId
        })
        }
        catch (e) {
            console.error(e)
            return {
                status: 500,
                body: {
                    message: 'Internal server error'
                }
            }
        }

    }

} as Actions
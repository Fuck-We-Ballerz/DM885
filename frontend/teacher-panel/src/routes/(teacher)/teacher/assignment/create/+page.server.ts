import { db } from '$lib';
import * as schema from '$lib/db/schema'
import { eq } from 'drizzle-orm';
import type { Actions } from './$types';

// type Course = typeof schema.course.$inferInsert;

export const actions = {
	newConfig: async () => {
        console.log("Creating new config")
        await db.insert(schema.assignmentConfig).values({
            max_cpu: 1, 
            max_ram: 1,
            max_submission: 1,
            max_time: "1",
        })
    },
    
    newAssignment: async ({ cookies, request }) => {
        const teacherUsername = cookies.get('kc-username')!
        const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})

		const data = await request.formData();
        
        const course_id = parseInt(data.get('course')!.toString())
        const config_id = parseInt(await data.get('assignmentConfig')!.toString());

        console.log("Creating new assignment");
        const insertedAssignment = await db.insert(schema.assignment).values({
            course_id: course_id,
            config_id: config_id,
            is_visible: true,
            title: data.get('title')!.toString(),
            docker_image: data.get('docker-image')!.toString(),
            start_date: data.get('startDate')!.toString(),
            end_date: data.get('dueDate')!.toString(),
        }).returning()

        await db.insert(schema.teacher_to_assignment).values({ 
            teacher_id: teacher!.id, 
            assignment_id: insertedAssignment[0].id
         })

        return { success: true };
	},

    deleteConfig: async ({ request }) => {
        const data = await request.formData();
        const id = parseInt(data.get('id')!.toString());


        console.log("Deleting all assignments related to config"); 
        await db.delete(schema.assignment).where(eq(schema.assignment.config_id, id));

        console.log("Deleting config");
        await db.delete(schema.assignmentConfig).where(eq(schema.assignmentConfig.id, id)); 
    }
} satisfies Actions;



import type { PageServerLoad } from './$types';
export const load: PageServerLoad = async ({cookies}) => {
    const teacherUsername = cookies.get('kc-username')!
    const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})
    
    const configs = await db.query.assignmentConfig.findMany()

    const courses = await db.select().from(schema.course)
                            .innerJoin(schema.teacher_to_course, eq(schema.course.id, schema.teacher_to_course.course_id))
                            .where(eq(schema.teacher_to_course.teacher_id, teacher!.id));

	return {
        courses: courses.map(courseObj => courseObj.course),
	    assignmentConfigs2: configs
	}
}
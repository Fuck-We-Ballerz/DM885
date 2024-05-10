import { db } from '$lib';
import * as schema from '$lib/db/schema'
import { eq } from 'drizzle-orm';
import type { Actions } from './$types';

type Course = typeof schema.course.$inferInsert;

export const actions = {
	newConfig: async () => {
        console.log("Creating new config")
        await db.insert(schema.assignmentConfig).values({
            name: "Some Awesome Config",
            max_cpu: 1,
            max_ram: 1,
            max_submission: 1,
            max_time: 1,
        })
    },
    
    newAssignment: async ({ cookies, request }) => {
		const data = await request.formData();
        
        // const course_id = await db.query.course.findFirst(
        //     { where: eq(schema.course.name, data.get('id')!.toString()) });
        console.log("assignment Config");
        console.log();
        
        const course_id = 1; // We probably wont support more courses
        const config_id = parseInt(await data.get('assignmentConfig')!.toString());
        // const config = await db.query.assignmentConfig.findFirst(
        //         { where: eq(schema.assignmentConfig.name, data.get('assignmentConfig')!.toString()) });
        // console.log(config);
        //TODO: Handle the form data. Insert into database.
        await db.insert(schema.assignment).values({
            course_id: course_id,
            config_id: config_id,
            is_visible: true,
            title: data.get('title')!.toString(),
            docker_image: data.get('docker-image')!.toString(),
            start_date: data.get('startDate')!.toString(),
            end_date: data.get('dueDate')!.toString(),
        });
        console.log(data);
        return { success: true };
	},
} satisfies Actions;



import type { PageServerLoad } from './$types';
export const load: PageServerLoad = async () => {
    const configs = await db.query.assignmentConfig.findMany()
	return {
	    assignmentConfigs2: configs
	};
};
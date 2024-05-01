import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import type { PageServerLoad } from './$types';

import postgres from 'postgres';

const queryClient = postgres('postgres://admin:admin@postgres-application:5432/postgres')

const db = drizzle(queryClient, {schema: {...schema}});

export const load: PageServerLoad = async ({params}) => {
    // const date = new Date()
    // date.toISOString()

    // const course = await db.insert(schema.course).values({
    //     name: "DM885"
    // }).returning()

    // await db.insert(schema.assignmentConfig).values({
    //     max_cpu: 1,
    //     max_ram: 1,
    //     max_submission: 1,
    //     max_time: 1,
    // })

    // await db.insert(schema.assignment).values ({
    //     config_id: 1,
    //     is_visible: false,
    //     start_date: date.toISOString(),
    //     end_date: date.toISOString(),
    //     title: "First assignment",
    //     course_id: 1
    // })
    
    
    let output = []
    const res = await db.query.assignment.findMany() ?? [];

    output = res.map((ass) => {
        return {
            title: ass.title,
            course: `Course: ${ass.course_id}`,
            config: `Config: ${ass.config_id}`,
            isVisible: ass.is_visible,
            startDate: ass.start_date,
            endDate: ass.end_date
        }
    });
	// We need to know which teacher we are.
    // To be able to get the assignments for the teacher.
    return {
        assignments: output
	};
};
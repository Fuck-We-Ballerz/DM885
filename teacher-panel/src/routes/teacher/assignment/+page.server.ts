import { PgTable } from 'drizzle-orm/pg-core';
import type { PageLoad } from './$types';

import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import type { PageServerLoad } from './$types';




// import { migrate } from 'drizzle-orm/postgres-js/migrator';
import postgres from 'postgres';

const queryClient = postgres('postgres://admin:admin@postgres_application:5432/testdb')

const db = drizzle(queryClient, {schema: {...schema}});

export const load: PageServerLoad = async ({params}) => {
    // const date = new Date()
    // date.toISOString()
    // await db.insert(schema.assignment).values ({
    //     config_id: 1,
    //     is_visible: false,
    //     start_date: date.toISOString(),
    //     end_date: date.toISOString()
    // })
    
    
    // await db.insert(schema.assignmentConfig).values({
    //     max_cpu: 1,
    //     max_ram: 1,
    //     max_submission: 1,
    //     max_time: 1,
    // })
    let output = []
    const res = await db.query.assignment.findMany() ?? [];

    output = [...res]

    console.log(`Result from db: ${output}`);
    for ( const i in output ) {
        console.log(output[i])
    }

	// We need to know which teacher we are.
    // To be able to get the assignments for the teacher.
    return {
        assignments: output
	//     assignmnets: [
    //         {
    //             title: `Assignment1`,
    //             course: `DM861`,
    //             config: `Config1`,
    //             isVisible: true,
    //             startDate: `2021-09-01`,
    //             endDate: `2021-09-15`,
    //         },
    //         {
    //             title: `Assignment2`,
    //             course: `DM535`,
    //             config: `Config1`,
    //             isVisible: true,
    //             startDate: `2021-09-08`,
    //             endDate: `2021-09-10`,
    //         },
    //         {
    //             title: `Assignment3`,
    //             course: `DM882`,
    //             config: `Config2`,
    //             isVisible: false,
    //             startDate: `2021-10-01`,
    //             endDate: `2021-12-15`,
    //         },
    //    ]
	};
};
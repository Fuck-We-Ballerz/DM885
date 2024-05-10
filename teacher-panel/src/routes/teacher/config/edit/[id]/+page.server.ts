import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import type { PageServerLoad } from './$types';
import type { Actions } from './$types';
import { db } from '$lib';
import { eq } from 'drizzle-orm';
import { error } from '@sveltejs/kit';

export const actions = {
    default: async ({params, request}) => {
        const data = await request.formData();
        
        await db.update(schema.assignmentConfig).set({
            
            max_cpu: parseInt(data.get('max_cpu')!.toString()),
            max_ram: parseInt(data.get('max_ram')!.toString()),
            max_time: data.get('max_time')!.toString(),
            max_submission: parseInt(data.get('max_submission')!.toString()),
        }).where(eq(schema.assignmentConfig.id, params.id));
    }
} satisfies Actions;

export const load: PageServerLoad = async ({params}) => {
    const config = await db.query.assignmentConfig.findFirst({where: eq(schema.assignmentConfig.id, params.id)})
    
    if (!config) {
        error(404, "Did not find any configuration with that ID");
    }
    
    const parts = config.max_time.split(':');

    let hours = parseInt(parts[0]);
    let minutes = parseInt(parts[1]);
    let seconds = parseInt(parts[2]);
    const total = hours * 3600 + minutes * 60 + seconds;

    return { data: {
        max_cpu: config.max_cpu,
        max_ram: config.max_ram,
        max_time: total,
        max_submission: config.max_submission
    }, copy: config };
};
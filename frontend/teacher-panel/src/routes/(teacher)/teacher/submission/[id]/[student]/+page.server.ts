import { and, eq } from 'drizzle-orm';
import * as schema from '$lib/db/schema'
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib';


export const load: PageServerLoad = async ({params}) => {   
    const student = await db.query.student.findFirst({where: eq(schema.student.id, parseInt(params.student))})
    const submissions = await db.select().from(schema.submission).where(and(eq(schema.submission.assignment_id, parseInt(params.id)),eq(schema.submission.student_id, parseInt(params.student))))

    const studentSubmissions = await Promise.all(submissions.map(async (submission) => {
        return {
            id: submission.id,
            grade: submission.grade,
            status: submission.status,
            submission_std: submission.submission_std,
            submission_err: submission.submission_err,
            submission_time: submission.submission_time
        }
    }))
    
    return {
        submissions: studentSubmissions.sort((a, b) => b.id - a.id),
        studentName: student!.name
	};
};


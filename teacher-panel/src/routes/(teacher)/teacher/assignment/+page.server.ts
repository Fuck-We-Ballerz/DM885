import { eq } from 'drizzle-orm';
import { drizzle } from 'drizzle-orm/postgres-js';
import * as schema from '$lib/db/schema'
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib';

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
    
    const configs = await db.query.assignmentConfig.findMany()

    let output = []
    const res = await db.query.assignment.findMany() ?? [];

    output = res.map((ass) => {
        return {
            title: ass.title,
            assignmentId: ass.id,
            course: ass.course_id,
            dockerImage: ass.docker_image,
            config: ass.config_id,
            isVisible: ass.is_visible,
            startDate: ass.start_date,
            endDate: ass.end_date
        }
    });
	// We need to know which teacher we are.
    // To be able to get the assignments for the teacher.
    return {
        assignmentConfigs: configs,
        assignments: output
	};
};


export const actions = {
    updateAssignment: async ({cookies, request}) => {
        // const token = cookies.get('kc-cookie');
        // console.log(token)
        console.log("update")

        const data = await request.formData();
        console.log(data)
        const assignmentId = parseInt(data.get("assignmentId")!.toString())

        const oldAssignment = await db.select().from(schema.assignment).where(eq(schema.assignment.id, assignmentId));
        console.log(oldAssignment[0].start_date);

        
        let isVisible = true
        if(data.get("isVisible")!.toString() === "false")
            isVisible = false            

        let startDate = data.get("startDate")!.toString()
        if(data.get("startDate")!.toString() === "")
            startDate = oldAssignment[0].start_date

        let endDate = data.get("endDate")!.toString()
        if(data.get("endDate")!.toString() === "")
            endDate = oldAssignment[0].end_date
        

        await db.update(schema.assignment).set({
            config_id: parseInt(data.get("assignmentConfig")!.toString()),
            is_visible: isVisible,
            docker_image: data.get('dockerImage')!.toString(),
            start_date: startDate,
            end_date: endDate,
        }).where(eq(schema.assignment.id, assignmentId))
    },

    deleteAssignment: async ({cookies, request}) => {
        // const token = cookies.get('kc-cookie');
        // console.log(token)
        console.log("delete")
        const data = await request.formData();
        console.log(data)
        const assignmentId = parseInt(data.get("assignmentId")!.toString())

        try {
            //foreign keys in following tables
            await db.delete(schema.submission).where(eq(schema.submission.assignment_id, assignmentId))
            await db.delete(schema.student_to_assignment).where(eq(schema.student_to_assignment.assignment_id, assignmentId))
            await db.delete(schema.teacher_to_assignment).where(eq(schema.teacher_to_assignment.assignment_id, assignmentId))

            //primary
            await db.delete(schema.assignment).where(eq(schema.assignment.id, assignmentId))

        } catch (error) {
            console.log(error);
        }
    }

} as Actions;
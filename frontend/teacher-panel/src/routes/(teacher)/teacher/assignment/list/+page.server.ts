import { eq } from 'drizzle-orm';
import * as schema from '$lib/db/schema'
import type { Actions, PageServerLoad } from './$types';
import { db } from '$lib';

export const load: PageServerLoad = async ({cookies, params}) => {   
    const teacherUsername = cookies.get('kc-username')!
    const teacher = await db.query.teacher.findFirst({ where: eq(schema.teacher.username, teacherUsername)})
    console.log(teacher)

    const configs = await db.query.assignmentConfig.findMany()

    let output = []
    //Get all assignments that a teacher has
    const res = await db.select().from(schema.assignment)
                        .innerJoin(schema.teacher_to_assignment, eq(schema.assignment.id, schema.teacher_to_assignment.assignment_id))
                        .where(eq(schema.teacher_to_assignment.teacher_id, teacher!.id))

    console.log(res)
    
    output = await Promise.all(res.map(async (ass) => {
        const courseName = await db.query.course.findFirst({ where: eq(schema.course.id, ass.assignment.course_id)})

        return {
            title: ass.assignment.title,
            assignmentId: ass.assignment.id,
            course: ass.assignment.course_id,
            courseName: courseName!.name,
            dockerImage: ass.assignment.docker_image,
            config: ass.assignment.config_id,
            isVisible: ass.assignment.is_visible,
            startDate: ass.assignment.start_date,
            endDate: ass.assignment.end_date
        }
    }))

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
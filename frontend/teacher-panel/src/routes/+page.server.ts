import type { PageServerLoad } from './$types';
import { PUBLIC_STUDENT_LOGIN_URL } from '$env/static/public'

export const load: PageServerLoad = async () => {
    let studentUrl = PUBLIC_STUDENT_LOGIN_URL
    return {
        studentUrl: studentUrl,
    }
}
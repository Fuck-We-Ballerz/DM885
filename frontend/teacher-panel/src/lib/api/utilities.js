import JSZip from "jszip";

export const zipSubmissions = async (/** @type {string | any[]} */ submissions) => {

    const zip = new JSZip();

    for (let i = 0; i < submissions.length; i += 1) {
        const submission = submissions[i];
        const student_folder = zip.folder(`student_${submission.student_id}`);
        if (!student_folder) {
            return new Response(JSON.stringify({
                message: `Failed to create folder for student ${submission.student_id}`
            }), { status: 500 });
        }
        student_folder.file("stdout.txt", submission.stdout);
        student_folder.file("stderr.txt", submission.stderr);
    }

    const zipFile = await zip.generateAsync({ type: "blob" });
    return zipFile;
}
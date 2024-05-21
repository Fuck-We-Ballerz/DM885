import { mkConfig, generateCsv, download } from "export-to-csv";
import JSZip from 'jszip';
import { saveAs } from 'file-saver';


export const getCSV = (data: { studentName: string; id: number; grade: string; submissionTime: string; status: string; }[], singlteStudent: boolean): void => {
    let filename = "metadata";

    if(singlteStudent){
        filename = `metadata_student_${data[0].id}`;
    }

    const csvConfig = mkConfig({filename: filename, useKeysAsHeaders: true });
    const csv = generateCsv(csvConfig)(data);
    const csvBtn = document.querySelector("#csv");

    try {
        csvBtn!.addEventListener("click", () => download(csvConfig)(csv));
    } catch (error) {
        console.error("Failed to add event listener or download CSV:", error);
    }
}

export const getZIP = async (data: { studentName: string; id: number; std: string; err: string; }[], singleStudent: boolean): Promise<void> => {
    let filename = "logs";

    if(singleStudent){
        filename = `logs_student_${data[0].id}`;
    }

    const zip = new JSZip();

    // Add files to the zip. This is just an example, you would need to adjust this to match your actual data.
    data.forEach((item) => {
        zip.file(`${filename}_submissionId_${item.id}.txt`, JSON.stringify(item));
    });

    const zipBtn = document.querySelector("#zip");

    try {
        zipBtn!.addEventListener("click", async () => {
            const content = await zip.generateAsync({type:"blob"});
            saveAs(content, `${filename}.zip`);
        });
    } catch (error) {
        console.error("Failed to add event listener or generate or download ZIP:", error);
    }
}
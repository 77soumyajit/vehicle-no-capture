import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export const downloadGatePass = async () => {

    const element = document.getElementById(
        "gate-pass-template"
    );

    if (!element) return;

    const canvas = await html2canvas(
        element,
        {
            scale: 3,
            useCORS: true,
            backgroundColor: "#ffffff",
        }
    );

    const image = canvas.toDataURL(
        "image/png"
    );

    const pdf = new jsPDF(
        "portrait",
        "mm",
        "a4"
    );

    const pdfWidth =
        pdf.internal.pageSize.getWidth();

    const pdfHeight =
        (canvas.height * pdfWidth) /
        canvas.width;

    pdf.addImage(
        image,
        "PNG",
        0,
        10,
        pdfWidth,
        pdfHeight
    );

    pdf.save("GatePass.pdf");

};
export const printGatePass = async () => {

    const element = document.getElementById(
        "gate-pass-template"
    );

    if (!element) return;

    const canvas = await html2canvas(
        element,
        {
            scale: 3,
            useCORS: true,
            backgroundColor: "#ffffff",
        }
    );

    const image = canvas.toDataURL(
        "image/png"
    );

    const printWindow = window.open(
        "",
        "_blank",
        "width=900,height=700"
    );

    printWindow.document.write(`
        <html>
        <head>
            <title>Gate Pass</title>

            <style>

                body{

                    margin:0;

                    display:flex;

                    justify-content:center;

                    align-items:center;

                    background:white;

                }

                img{

                    width:95%;

                }

            </style>

        </head>

        <body>

            <img src="${image}" />

        </body>

        </html>
    `);

    printWindow.document.close();

    printWindow.focus();

    printWindow.onload = () => {

        printWindow.print();

        printWindow.close();

    };

};
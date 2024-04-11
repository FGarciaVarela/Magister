import React from 'react';
import { useHistoryContext } from './historyContext';
import jsPDF from 'jspdf';

function HistoryPage() {
  const { history } = useHistoryContext();

  const downloadPDF = () => {
    const doc = new jsPDF();
    let y = 20; // Initial vertical position

    doc.setFontSize(16);
    doc.setFont(undefined, 'bold');
    doc.text('History', 10, 10);
    y += 10; // Increase Y coordinate to leave a gap after the title

    doc.setFontSize(12);
    doc.setFont(undefined, 'normal');

    history.forEach((entry, index) => {
      // Check if we need to add a new page
      if (y > 280) {
        doc.addPage();
        y = 10; // Reset Y position for the new page
      }

      const entryNumber = `${index + 1}. `; // Create the entry number string
      const inputText = `Input Text: ${entry.inputText}`;
      const abstractWords = `Abstract Words: ${entry.abstractWords.join(', ')}`;

      // Combine the entry number with the input text
      const combinedText = `${entryNumber}${inputText}`;
      const inputTextLines = doc.splitTextToSize(combinedText, 190); // Ensure text wrapping
      doc.text(inputTextLines, 10, y);
      y += inputTextLines.length * 7; // Adjust Y based on the number of lines

      // Continue with abstract words as before
      const abstractWordsLines = doc.splitTextToSize(abstractWords, 190);
      doc.text(abstractWordsLines, 10, y);
      y += abstractWordsLines.length * 7 + 10; // Extra space after each entry
    });

    doc.save('history.pdf');
  };


  return (
    <div>
      <h2>History</h2>
      <button onClick={downloadPDF}>Download PDF</button>
      {history.map((entry, index) => (
        <div key={index}>
          <p>Input Text: {entry.inputText}</p>
          <p>Abstract Words: {entry.abstractWords.join(', ')}</p>
          <hr />
        </div>
      ))}
    </div>
  );
}

export default HistoryPage;

import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  // Asegúrate de que abstractWords sea manejado como un array
  const [abstractWords, setAbstractWords] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [timeTaken, setTimeTaken] = useState(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    const savedInputText = localStorage.getItem('inputText');
    const savedAbstractWords = localStorage.getItem('abstractWords');
    if (savedInputText) setInputText(savedInputText);
    // Asegura que savedAbstractWords sea una cadena válida de JSON antes de analizarla
    if (savedAbstractWords && savedAbstractWords !== "undefined") {
      try {
        const parsedAbstractWords = JSON.parse(savedAbstractWords);
        if (Array.isArray(parsedAbstractWords)) { // Verifica que sea un array
          setAbstractWords(parsedAbstractWords);
        }
      } catch (e) {
        console.error("Error parsing abstractWords from localStorage:", e);
        // Manejo opcional del error, por ejemplo, limpiar localStorage si es necesario
      }
    }
  }, []);


  useEffect(() => {
    localStorage.setItem('inputText', inputText);
  }, [inputText]);

  useEffect(() => {
    localStorage.setItem('abstractWords', JSON.stringify(abstractWords));
  }, [abstractWords]);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
    const textarea = textareaRef.current;
    textarea.style.height = 'inherit';
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const startTime = performance.now();
    try {
      const response = await fetch(`${import.meta.env.VITE_REACT_APP_API_URL}/detect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          mode: 'no-cors',
        },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      // Asumimos que data.abstractWords ya es un array
      setAbstractWords(data.abstractWords);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      const endTime = performance.now();
      setTimeTaken(((endTime - startTime) / 1000).toFixed(2));
      setIsLoading(false);
    }
  };

  // Procesa el texto de entrada para ennegrecer las palabras abstractas
  const processedText = inputText.split(/\s+/).map((word, index) => (
    abstractWords.includes(word.toLowerCase()) ?
      <span key={index} style={{ fontWeight: 'bold' }}>{word} </span> :
      word + ' '
  ));

  return (
    <div className="App">
      <main>
        <form onSubmit={handleSubmit} className="form-container">
          <div className="textarea-container">
            <textarea
              ref={textareaRef}
              value={inputText}
              onChange={handleInputChange}
              lang="en"
              placeholder="Write your sentence here..."
            />
            <button type="submit" className="submitButton">Detect</button>
          </div>
          <div className="text-output-container">

            {processedText}
          </div>
        </form>
        {isLoading && <p className="loading">Processing...</p>}
        {!isLoading && timeTaken && (
          <div className="results">
            <p>Time load: {timeTaken} seconds</p>
            <p>Abstract Words: {`{${abstractWords.join(', ')}}`}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
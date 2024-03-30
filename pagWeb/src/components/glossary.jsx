import React, { useState } from 'react';
import './glossary.css';

function Glossary() {
  const [showModal, setShowModal] = useState(false);
  const [termDefinition, setTermDefinition] = useState('');
  const [selectedTerm, setSelectedTerm] = useState('');

  const handleTermClick = (term, definition) => {
    setSelectedTerm(term);
    setTermDefinition(definition);
    setShowModal(true);
  };

  const handleCloseClick = (e) => {
    e.stopPropagation(); // Previene la propagación del evento al overlay
    setShowModal(false);
    setSelectedTerm(''); // Resetea el término seleccionado cuando el modal se cierra
  };

  const handleOverlayClick = () => {
    setShowModal(false);
    setSelectedTerm(''); // Resetea el término seleccionado cuando se hace clic fuera
  };

  return (
    <div className="glossary">
      {showModal && (
        <div className="overlay" onClick={handleOverlayClick}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={handleCloseClick}>&times;</span>
            <p>{termDefinition}</p>
          </div>
        </div>
      )}
      <div
        className={`term ${selectedTerm === 'Abstract' ? 'selected' : ''}`}
        onClick={() => handleTermClick("Abstract", "Abstract language refers to intangible ideas or qualities, such as love, hate, or honor.")}>
        Abstract
      </div>
      <div
        className={`term ${selectedTerm === 'Concrete' ? 'selected' : ''}`}
        onClick={() => handleTermClick("Concrete", "Concrete words refer to tangible items, things you can count, touch, name, identify in time.  For example, phrases such as ten thousand, raw cherry wood, John Smith, and ten o’clock on January 12 are concrete.")}>
        Concrete
      </div>
    </div>
  );
}

export default Glossary;

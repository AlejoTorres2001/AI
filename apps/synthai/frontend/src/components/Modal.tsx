import React from 'react';
import '../styles/Modal.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  text: string;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, text }) => {
  

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal">
        <p>{text}</p>
      </div>
    </div>
  );
};

export default Modal;

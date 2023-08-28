import React from 'react';
import '../styles/QuestionButton.css';

interface QuestionButtonProps {
  onClick: () => void;
}

const QuestionButton: React.FC<QuestionButtonProps> = ({ onClick }) => {
  return (
    <button className="question-button" onClick={onClick}>
      ?
    </button>
  );
};

export default QuestionButton;

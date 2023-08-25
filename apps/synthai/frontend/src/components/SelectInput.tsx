import React from 'react';
import '../styles/SelectInput.css';

interface SelectInputProps {
  options: { value: string; label: string }[];
  value: string;
  id: string;
  name: string;
  onChange?: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
}

function SelectInput({ options, value, onChange,name,id }: SelectInputProps) {

  return (
    <select name={name} id={id} className="select-input" value={value} onChange={onChange}>
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

export default SelectInput;

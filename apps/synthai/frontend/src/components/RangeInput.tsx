import React from "react";
import "../styles/RangeInput.css"; // Make sure to import your CSS file

type RangeInputProps = {
  min: number;
  max: number;
  step: number;
  value: number;
  id: string;
  name: string;
  onChange?: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
} & React.InputHTMLAttributes<HTMLInputElement>;

function RangeInput({
  min,
  max,
  step,
  value,
  onChange,
  id,
  name,
}: RangeInputProps) {
  return (
    <div className="range-input-container">
      <input
        type="range"
        className="range-input"
        id={id}
        name={name}
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={onChange}
      />
      <span className="range-value">{value}</span>
    </div>
  );
}

export default RangeInput;

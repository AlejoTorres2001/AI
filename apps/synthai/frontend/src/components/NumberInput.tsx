import { InputHTMLAttributes } from "react";

import '../styles/NumberInput.css'; 
type NumberInputProps = {
  value: number;
  name: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
} & InputHTMLAttributes<HTMLInputElement>;
const NumberInput = ({ value, onChange,name,...rest }: NumberInputProps) => {
  return (
      <input
        type="number"
        value={value}
        name="name"
        onChange={onChange}
        className="number-input"
        {...rest}
      />
  );
};

export default NumberInput;

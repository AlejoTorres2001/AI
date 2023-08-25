import NumberInput from "./NumberInput";
import RangeInput from "./RangeInput";
import "../styles/Parameter.css";
import SelectInput from "./SelectInput";
interface ParameterProps {
  name: string;
  type: "text" | "number" | "checkbox" | "range" | "list";
  description: string;
  value: string | number | boolean;
  onChange?: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
  options?: { value: string; label: string }[];
}
function Parameter({
  name,
  type,
  description,
  value,
  onChange,
  options,
}: ParameterProps) {
  return (
    <div className="parameter-container">
      <label className="input-label" htmlFor={name}>
        {description}
      </label>
      {type === "text" && (
        <input
          type="text"
          name={name}
          id={name}
          value={value as string}
          onChange={onChange}
        />
      )}
      {type === "number" && (
        <NumberInput
          name={name}
          id={name}
          value={value as number}
          onChange={onChange}
        />
      )}
      {type === "checkbox" && (
        <input
          type="checkbox"
          id={name}
          value={name}
          checked={value as boolean}
          onChange={onChange}
          name={name}
        />
      )}
      {type === "range" && (
        <RangeInput
          id={name}
          name={name}
          value={value as number}
          onChange={onChange}
          min={0}
          max={1}
          step={0.01}
        />
      )}
      {type === "list" && (
        <SelectInput options={options as { value: string; label: string }[]} value={value as string} id={name} name={name} onChange={onChange} />
      )}
    </div>
  );
}

export default Parameter;

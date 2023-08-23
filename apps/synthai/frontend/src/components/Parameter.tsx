interface ParameterProps {
  name: string;
  type: "text" | "number" | "checkbox" | "range" | "list";
  description: string;
  value: string | number | boolean;
  onChange?: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  options?: string[];
}
function Parameter({ name, type, description, value,onChange,options }: ParameterProps) {
  return (
    <div>
      <label htmlFor={name}>{description}</label>
      {type === "text" && (
        <input type="text" name={name} id={name} value={value as string} onChange={onChange} />
      )}
      {type === "number" && (
        <input type="number" name={name} id={name} value={value as number} onChange={onChange} />
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
        <input
          type="range"
          id={name}
          name={name}
          value={value as number}
          onChange={onChange}
        />
      )}
      {type === "list" && (
        <select name={name} id={name} onChange={onChange}>
          {options?.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}

export default Parameter;

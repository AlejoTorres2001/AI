import React from "react";
import { Parameters } from "../models/parameters";
interface ParametersCustomizerProps {
  parameters: Parameters;
  setParameters: React.Dispatch<React.SetStateAction<Parameters>>;
  children: React.ReactNode;
}
function ParametersCustomizer({
  children,
  parameters,
  setParameters,
}: ParametersCustomizerProps) {
  return (
    <div>
      <h2>Parameters</h2>
      {children}
    </div>
  );
}

export default ParametersCustomizer;

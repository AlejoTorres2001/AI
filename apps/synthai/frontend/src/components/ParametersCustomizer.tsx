import React, { ChangeEvent, ReactElement } from "react";
import "../styles/ParametersCustomizer.css";
interface ParametersCustomizerProps {
  handleParametersChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
  children: React.ReactNode;
}
type ChildWithOnChange = ReactElement & {
  props: {
    onChange: (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  };
};

function ParametersCustomizer({
  children,
  handleParametersChange,
}: ParametersCustomizerProps) {
  const childrenWithProps = React.Children.map(children, (child) => {
    if (React.isValidElement(child)) {
      const childWithOnChange = child as ChildWithOnChange;
      return React.cloneElement(childWithOnChange, {
        onChange: handleParametersChange,
      });
    }
    return child;
  });

  return (
    <section className="parameters-section">
      <div className="parameters-container">
        <h2>Customize Parameters</h2>
        {childrenWithProps}
      </div>
    </section>
  );
}

export default ParametersCustomizer;

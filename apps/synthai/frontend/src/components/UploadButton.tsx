import React from "react";
interface uploadButtonProps {
  handleSubmit: (e: React.MouseEvent<HTMLElement>) => void;
}
function UploadButton({ handleSubmit }: uploadButtonProps) {
  return (
    <div>
      <button onClick={handleSubmit}>
        Upload
      </button>
    </div>
  );
}

export default UploadButton;

import { useRef } from "react";
import "../styles/FileSelector.css";

interface FileSelectorProps {
  handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  selectedFileName: string;
}
function FileSelector({ handleFileChange, selectedFileName }: FileSelectorProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const handleChooseFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  return (
    <div className="file-input-container">
      <div className="custom-file-input" onClick={handleChooseFile}>
        {selectedFileName && (<span className="file-name">Succesfully loaded file: {selectedFileName}</span>)}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          />
      </div>
    </div>
  );
}

export default FileSelector;

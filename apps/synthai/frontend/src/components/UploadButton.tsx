import "../styles/UploadButton.css";
interface uploadButtonProps {
  handleSubmit: (e: React.MouseEvent<HTMLElement>) => void;
}
function UploadButton({ handleSubmit }: uploadButtonProps) {
  return (
    <div className="button-container">
      <button onClick={handleSubmit} className="upload-button">
        Summarize Document 
      </button>
    </div>
  );
}

export default UploadButton;

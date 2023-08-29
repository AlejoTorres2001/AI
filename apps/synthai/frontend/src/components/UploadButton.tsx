import "../styles/UploadButton.css";
interface uploadButtonProps {
  handleSubmit: (e: React.MouseEvent<HTMLElement>) => void;
}
function UploadButton({ handleSubmit }: uploadButtonProps) {
  return (
    <button onClick={handleSubmit} className="upload-button">
      Summarize Document
    </button>
  );
}

export default UploadButton;

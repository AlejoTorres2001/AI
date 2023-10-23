import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopy, faCheck } from "@fortawesome/free-solid-svg-icons";
import { toast } from "react-toastify";
interface CopyToClipboardButtonProps {
  textToCopy: string;
}
const CopyToClipboardButton = ({ textToCopy }: CopyToClipboardButtonProps) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard
      .writeText(textToCopy)
      .then(() => {
        setCopied(true);
        toast.success("Copied to clipboard");
        setTimeout(() => setCopied(false), 5500);
      })
      .catch(() => toast.error("Error copying to clipboard"));
  };

  return (
    <button onClick={copyToClipboard} className="download-button">
      {copied ? (
        <FontAwesomeIcon icon={faCheck} className="icon" />
      ) : (
        <FontAwesomeIcon icon={faCopy} className="icon" />
      )}
    </button>
  );
};

export default CopyToClipboardButton;

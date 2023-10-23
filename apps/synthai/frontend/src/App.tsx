import { useState } from "react";
import "./styles/App.css";
import { summarize } from "./services/summarize";
import FileSelector from "./components/FileSelector";
import { Parameters, defaultParameters } from "./models/parameters";
import ParametersCustomizer from "./components/ParametersCustomizer";
import Parameter from "./components/Parameter";
import UploadButton from "./components/UploadButton";
import QuestionButton from "./components/QuestionButton";
import Modal from "./components/Modal";
import Spinner from "./components/Spinner";
import PDFDownload from "./components/PDFDownload";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import CopyToClipboardButton from "./components/CopyToClipboardButton";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [parameters, setParameters] = useState<Parameters>(defaultParameters);
  const [isLoading, setIsLoading] = useState(false);

  const [summary, setSummary] = useState("");
  const handleSubmit = async (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      if (file === null) {
        toast.error(`Please select a file`);
        return;
      }
      const data = await summarize(file, parameters);
      if (!data.ok) {
        toast.error(data.message);
        return;
      }
      setSummary(data.summary);
      toast.success(data.message);
    } catch (error) {
      toast.error(`Error generating summary`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const fileName = e.target.files[0]?.name || "No file selected";
      setFile(e.target.files[0]);
      setSelectedFileName(fileName);
    }
  };

  const handleParametersChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setParameters((prevData) => ({
      ...prevData,
      [name]: type === "number" || type === "range" ? Number(value) : value,
    }));
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="main">
      <QuestionButton onClick={openModal} />
      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <section>1. Select your PDF file</section>
        <section>2. Customize the workflow parameters</section>
        <section>3. Summarize your document!</section>
      </Modal>
      <div className="grid">
        <FileSelector
          handleFileChange={handleFileChange}
          selectedFileName={selectedFileName}
        />

        <ParametersCustomizer handleParametersChange={handleParametersChange}>
          <Parameter
            name="max_sequence_length"
            type="number"
            description="Max Tokens"
            value={parameters.max_sequence_length}
          />
          <Parameter
            name="temperature"
            type="range"
            description="Temperature"
            value={parameters.temperature}
          />
          <Parameter
            name="clusters_number"
            type="number"
            description="clusters number"
            value={parameters.clusters_number}
          />
          <Parameter
            name="language"
            type="list"
            description="language"
            value={parameters.language}
            options={[
              { value: "EN", label: "EN" },
              { value: "SP", label: "SP" },
            ]}
          />
          <Parameter
            name="chunk_size"
            type="number"
            description="chunk size"
            value={parameters.chunk_size}
          />
          <Parameter
            name="chunk_overlap"
            type="number"
            description="chunk overlap"
            value={parameters.chunk_overlap}
          />
          <Parameter
            name="from_page"
            type="number"
            description="from page"
            value={parameters.from_page}
          />
          <Parameter
            name="to_page"
            type="number"
            description="to page"
            value={parameters.to_page}
          />
        </ParametersCustomizer>
        <div className="button-container">
          <UploadButton handleSubmit={handleSubmit} />
          {summary && (
            <div className="inner-button-container">
              <PDFDownload
                summary={summary}
                selectedFileName={selectedFileName}
              />
              <CopyToClipboardButton textToCopy={summary} />
            </div>
          )}
        </div>
      </div>
      {isLoading && <Spinner />}
      <ToastContainer closeOnClick theme="dark" />
    </div>
  );
}

export default App;

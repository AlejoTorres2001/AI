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
function App() {
  const [file, setFile] = useState<File | null>(null);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [parameters, setParameters] = useState<Parameters>(defaultParameters);
  const [isLoading, setIsLoading] = useState(false);

  const [message, setMessage] = useState("");
  const [summary, setSummary] = useState("");
  const handleSubmit = async (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      if (file === null) return;
      const data = await summarize(file, parameters);
      setMessage(data.message);
      if (data.ok) {
        setSummary(data.summary);
      }
    } catch (error) {
      console.error("Error occurred:", error);
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
    console.log(name, value, type);
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
      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        text="This is some modal text."
      />
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
            name="top_k"
            type="range"
            description="Top K"
            value={parameters.top_k}
          />
          <Parameter
            name="top_p"
            type="range"
            description="Top P"
            value={parameters.top_p}
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
          value={parameters.from_page}/>
          <Parameter
          name="to_page"
          type="number"
          description="to page"
          value={parameters.to_page}/>
        </ParametersCustomizer>
        <div className="button-container">
          <UploadButton handleSubmit={handleSubmit} />
          {summary && (
            <PDFDownload
              summary={summary}
              selectedFileName={selectedFileName}
            />
          )}
        </div>
      </div>
      {isLoading && <Spinner />}
      {message && <p>{message}</p>}
      <div></div>
    </div>
  );
}

export default App;

import { useState } from "react";
import "./styles/App.css";
import { summarize } from "./services/summarize";
import FileSelector from "./components/FileSelector";
import { Parameters, defaultParameters } from "./models/parameters";
import ParametersCustomizer from "./components/ParametersCustomizer";
import Parameter from "./components/Parameter";
import UploadButton from "./components/UploadButton";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [selectedFileName, setSelectedFileName] = useState("");

  const [parameters, setParamaters] = useState<Parameters>(defaultParameters);

  const [message, setMessage] = useState<string>("");

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
    setParamaters((prevData) => ({
      ...prevData,
      [name]: type === "number" || type === "range" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    const data = await summarize(file as File, parameters);
    setMessage(data.message);
    if (data.ok) {
      console.log("this is the summary", data.summary);
    }
  };

  return (
    <div className="main">
      <div className="grid">
        <FileSelector
          handleFileChange={handleFileChange}
          selectedFileName={selectedFileName}
        />
        <ParametersCustomizer handleParametersChange={handleParametersChange}>
          <Parameter
            name="max_sequence_length"
            type="number"
            description="Max Sentences"
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
            options={["EN", "SP"]}
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
        </ParametersCustomizer>
        <UploadButton handleSubmit={handleSubmit} />
      </div>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;

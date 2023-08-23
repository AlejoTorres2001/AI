import { useState } from "react";
import "./styles/App.css";
import { summarize } from "./services/summarize";
import FileSelector from "./components/FileSelector";
import { Parameters, defaultParameters } from "./models/parameters";
import ParametersCustomizer from "./components/ParametersCustomizer";

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

  const handleJsonChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setParamaters((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
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
        <ParametersCustomizer parameters={parameters} setParameters={setParamaters}>
        <h3>Parametro1</h3>
        <h3>Parametro2</h3>
        <h3>Parametro3</h3>
        </ParametersCustomizer>
        <button type="submit" onClick={handleSubmit}>
          Upload
        </button>
      </div>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;

import { useState } from 'react'
import './App.css'
import { summarize } from './services/summarize';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [parameters, setParamaters] = useState<Record<string, any>>({});
  const [message, setMessage] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleJsonChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setParamaters(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
      const data = await summarize(file as File, parameters);
      setMessage(data.message);
      if (data.ok) {
        console.log("this is the summary",data.summary)
      }
  };

  return (
    <>
      <div className="card">
      <h1>Upload File and JSON Data</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <br />
        <input
          type="text"
          name="key1"
          placeholder="Key 1"
          onChange={handleJsonChange}
        />
        <input
          type="text"
          name="key2"
          placeholder="Key 2"
          onChange={handleJsonChange}
        />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
      </div>
    </>
  )
}

export default App

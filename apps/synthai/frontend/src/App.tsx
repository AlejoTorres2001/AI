import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';
interface JsonResponse {
  message: string;
  json_data: Record<string, any>;
}
function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jsonData, setJsonData] = useState<Record<string, any>>({});
  const [message, setMessage] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleJsonChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setJsonData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('file', file as File);
    formData.append('data', JSON.stringify({ json_data: jsonData }));

    try {
      const response = await axios.post<JsonResponse>('http://localhost:8000/upload', formData, {
         headers: {
           'Content-Type': 'multipart/form-data',
         },
      });
      setMessage(response.data.message);
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
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

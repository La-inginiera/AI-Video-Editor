import React, { useState } from 'react';
import axios from '../services/api';

function VideoUploader({ setOriginalVideo, onUploadComplete }) {  // Accept onUploadComplete as a prop
  const [videoFile, setVideoFile] = useState(null);
  const [prompt, setPrompt] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setVideoFile(file);
    if (file) {
      // Set the original video URL for preview in the parent component
      setOriginalVideo(URL.createObjectURL(file));
    }
  };

  const handlePromptChange = (e) => {
    setPrompt(e.target.value);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('video', videoFile);
    formData.append('prompt', prompt);

    try {
      const response = await axios.post('/upload', formData);
      console.log('Video uploaded:', response.data);

      // Notify the parent that the upload is complete and the processing has started
      onUploadComplete();  // This triggers status tracking in the parent
    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  return (
    <div className="mb-6">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Upload Video & Provide Prompt</h2>
      <div className="flex flex-col space-y-4">

        <input
          type="file"
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-600 file:text-white
            hover:file:bg-blue-700"
          onChange={handleFileChange}
        />

        <input
          type="text"
          placeholder="Enter prompt (e.g., Add voiceover, blur sections)"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
          value={prompt}
          onChange={handlePromptChange}
        />

        {/* Display the uploaded video before the button */}
        {videoFile && (
          <video className="w-full rounded-lg shadow-md mb-4" controls>
            <source src={URL.createObjectURL(videoFile)} type="video/mp4" />
          </video>
        )}

        <button
          onClick={handleUpload}
          className="px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-all duration-300"
        >
          Upload & Process Video
        </button>
      </div>
    </div>
  );
}

export default VideoUploader;

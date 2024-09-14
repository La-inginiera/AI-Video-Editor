import React, { useState } from 'react';
import VideoUploader from './components/VideoUploader';
import VideoStatus from './components/VideoStatus';

function App() {
  const [originalVideo, setOriginalVideo] = useState(null); // State to store the original video URL
  const [startTracking, setStartTracking] = useState(false); // State to track processing status

  const handleUploadComplete = () => {
    setStartTracking(true);  // Start tracking status when upload is complete
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center">
      <h1 className="text-4xl font-bold text-blue-600 mb-6">Video Processing App</h1>
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-6">
        {/* Video Uploader Component */}
        <VideoUploader 
          setOriginalVideo={setOriginalVideo} 
          onUploadComplete={handleUploadComplete}  // Notify App when the upload is complete
        /> 

        {/* Video Processing Status */}
        {startTracking && <VideoStatus />}  {/* Only render VideoStatus when tracking is active */}
      </div>
    </div>
  );
}

export default App;

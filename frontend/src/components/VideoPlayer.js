import React, { useState } from 'react';
import axios from '../services/api';

function VideoPlayer() {
  const [videoUrl, setVideoUrl] = useState('');

  const handleGetProcessedVideo = async () => {
    try {
      const response = await axios.get('/process');
      setVideoUrl(response.data.video_path);
    } catch (error) {
      console.error('Error retrieving processed video:', error);
    }
  };

  return (
    <div className="mb-6">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">View Processed Video</h2>
      <button
        onClick={handleGetProcessedVideo}
        className="px-6 py-2 text-white bg-green-600 hover:bg-green-700 rounded-lg transition-all duration-300 mb-4"
      >
        Get Processed Video
      </button>
      {videoUrl && (
        <video controls className="w-full rounded-lg shadow-lg">
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      )}
    </div>
  );
}

export default VideoPlayer;

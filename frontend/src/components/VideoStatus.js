import React, { useEffect, useState } from 'react';

function VideoStatus() {
  const [progress, setProgress] = useState(0);
  const [processedVideo, setProcessedVideo] = useState(null);

  useEffect(() => {
    const eventSource = new EventSource('http://127.0.0.1:5000/status');

    eventSource.onmessage = (event) => {
      console.log('Receiving event: ', event);
      const data = JSON.parse(event.data);

      // Update progress with the streamed data
      setProgress(data.progress);

      // Check if the video is processed
      if (data.video) {
        setProcessedVideo(data.video);  // Use the base64-encoded video from backend
        eventSource.close();  // Close the event stream after receiving the final video
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();  // Clean up event source on component unmount
    };
  }, []);

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = processedVideo;
    link.download = 'processed_video.mp4'; // Set the desired file name
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="mb-6">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Processing Status</h2>

      {/* Progress Bar */}
      <div className="w-full bg-gray-300 rounded-lg">
        <div
          className="bg-green-500 text-xs font-medium text-white text-center p-0.5 leading-none rounded-lg"
          style={{ width: `${progress}%` }}
        >
          {progress}%
        </div>
      </div>

      {/* Show Processed Video and Download Button When Ready */}
      {processedVideo && (
        <div className="mt-4">
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Processed Video:</h3>
          <video className="w-full" controls>
            <source src={processedVideo} type="video/mp4" />
          </video>

          {/* Download Button */}
          <button
            onClick={handleDownload}
            className="mt-4 px-6 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-all duration-300"
          >
            Download Processed Video
          </button>
        </div>
      )}
    </div>
  );
}

export default VideoStatus;

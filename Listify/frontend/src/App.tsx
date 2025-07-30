import { useState, useEffect, useRef } from 'react';
import './App.css';

// Extend the window interface to include File System Access API
declare global {
  interface Window {
    showDirectoryPicker?: () => Promise<FileSystemDirectoryHandle>;
  }
}

// File System API types
interface FileSystemDirectoryHandle {
  name: string;
  kind: 'directory';
}

function App() {
  const [playlistId, setPlaylistId] = useState('');
  const [targetFolder, setTargetFolder] = useState('');
  const [isDownloading, setIsDownloading] = useState(false);
  const [progress, setProgress] = useState(0);
  const progressIntervalRef = useRef<number | null>(null);

  // Progress management effect
  useEffect(() => {
    if (isDownloading) {
      setProgress(0);
      // Increment progress from 0% to 98% over 60 seconds
      // 98% / 60000ms = 0.00163% per millisecond
      // We'll update every 100ms, so 0.163% per update
      const incrementPerUpdate = 98 / 600; // 600 updates over 60 seconds (every 100ms)

      progressIntervalRef.current = window.setInterval(() => {
        setProgress((prev) => {
          const newProgress = prev + incrementPerUpdate;
          return newProgress >= 98 ? 98 : newProgress;
        });
      }, 100);
    } else {
      // Clear interval when not downloading
      if (progressIntervalRef.current) {
        clearInterval(progressIntervalRef.current);
        progressIntervalRef.current = null;
      }
      setProgress(0);
    }

    // Cleanup function
    return () => {
      if (progressIntervalRef.current) {
        clearInterval(progressIntervalRef.current);
        progressIntervalRef.current = null;
      }
    };
  }, [isDownloading]);

  const handleFolderButtonClick = async () => {
    try {
      // Check if File System Access API is supported
      if (window.showDirectoryPicker) {
        const dirHandle = await window.showDirectoryPicker();

        // Set the folder name in the text field
        setTargetFolder(dirHandle.name);

        console.log('Selected directory:', dirHandle.name);
      } else {
        // Fallback for browsers that don't support the API
        const suggestedPath = `/Users/username/Downloads/Spotify-Music`;
        const userPath = prompt(
          "Your browser doesn't support modern folder selection. Please enter the full path where you want to save the downloaded music files:",
          suggestedPath
        );

        if (userPath && userPath.trim()) {
          setTargetFolder(userPath.trim());
        }
      }
    } catch (error) {
      console.log('Folder selection cancelled or failed:', error);
      // User cancelled the picker or an error occurred - do nothing
    }
  };

  const handleDownload = async () => {
    if (!playlistId || !targetFolder) {
      alert('Please provide both playlist ID and target folder');
      return;
    }

    setIsDownloading(true);

    try {
      const response = await fetch(`http://localhost:8000/download?playlist_id=${playlistId}&target_folder=${encodeURIComponent(targetFolder)}`);

      // Set progress to 100% when response is received
      setProgress(100);

      if (response.ok) {
        const result = await response.json();
        alert(`Download completed! Files saved to: ${result.download_path}`);
      } else {
        const error = await response.json();
        alert(`Download failed: ${error.detail}`);
      }
    } catch (error) {
      alert(`Error: ${error}`);
    } finally {
      // Small delay to show 100% before hiding overlay
      setTimeout(() => {
        setIsDownloading(false);
      }, 500);
    }
  };

  return (
    <>
      {isDownloading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Downloading playlist...</p>
          <div className="progress-container">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}></div>
            </div>
            <div className="progress-text">{Math.round(progress)}%</div>
          </div>
        </div>
      )}

      <div className="app">
        <div className="header">
          <h1>Listify</h1>
          <h2>Download Entire Playlists</h2>
        </div>

        <div className="form">
          <div className="input-group">
            <label htmlFor="playlist-id">Spotify Playlist ID:</label>
            <input id="playlist-id" type="text" value={playlistId} onChange={(e) => setPlaylistId(e.target.value)} placeholder="Enter Spotify playlist ID" />
          </div>

          <div className="input-group">
            <label htmlFor="target-folder">Target Folder (Full Path):</label>
            <div className="folder-input">
              <input
                id="target-folder"
                type="text"
                value={targetFolder}
                onChange={(e) => setTargetFolder(e.target.value)}
                placeholder="e.g., /Users/username/Downloads/MyMusic"
              />
              <button type="button" onClick={handleFolderButtonClick}>
                Choose Folder
              </button>
            </div>
          </div>

          <button className="download-btn" onClick={handleDownload} disabled={isDownloading || !playlistId || !targetFolder}>
            {isDownloading ? 'Downloading...' : 'Download Playlist'}
          </button>
        </div>
      </div>
    </>
  );
}

export default App;

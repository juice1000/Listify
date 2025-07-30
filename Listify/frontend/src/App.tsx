import { useState } from 'react';
import './App.css';
import spotifyLogo from './assets/spotify-logo.svg';

function App() {
  const [playlistId, setPlaylistId] = useState('');
  const [targetFolder, setTargetFolder] = useState('');
  const [isDownloading, setIsDownloading] = useState(false);

  const handleFolderSelect = async () => {
    try {
      // Check if the File System Access API is supported
      if ('showDirectoryPicker' in window) {
        const dirHandle = await (window as any).showDirectoryPicker();
        setTargetFolder(dirHandle.name);
      } else {
        // Fallback for browsers that don't support the API
        alert('Folder selection not supported in this browser. Please enter the folder path manually.');
      }
    } catch (error) {
      console.error('Error selecting folder:', error);
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
      setIsDownloading(false);
    }
  };

  return (
    <div className="app">
      <div className="header">
        <h1>Listify - Playlist Downloader</h1>
      </div>

      <div className="form">
        <div className="input-group">
          <label htmlFor="playlist-id">Spotify Playlist ID:</label>
          <input id="playlist-id" type="text" value={playlistId} onChange={(e) => setPlaylistId(e.target.value)} placeholder="Enter Spotify playlist ID" />
        </div>

        <div className="input-group">
          <label htmlFor="target-folder">Target Folder:</label>
          <div className="folder-input">
            <input id="target-folder" type="text" value={targetFolder} onChange={(e) => setTargetFolder(e.target.value)} placeholder="Select or enter folder path" />
            <button type="button" onClick={handleFolderSelect}>
              Choose Folder
            </button>
          </div>
        </div>

        <button className="download-btn" onClick={handleDownload} disabled={isDownloading || !playlistId || !targetFolder}>
          {isDownloading ? 'Downloading...' : 'Download Playlist'}
        </button>
      </div>
    </div>
  );
}

export default App;

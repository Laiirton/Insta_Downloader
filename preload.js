const { contextBridge, ipcRenderer, shell } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  downloadVideo: (url, savePath, format) => ipcRenderer.invoke('download-video', url, savePath, format),
  selectDirectory: () => ipcRenderer.invoke('select-directory'),
  closeApp: () => ipcRenderer.send('close-app'),
  minimizeApp: () => ipcRenderer.send('minimize-app'),
  onDownloadProgress: (callback) => ipcRenderer.on('download-progress', (event, progress) => callback(progress)),
  openExternalLink: (url) => shell.openExternal(url),
  moveWindow: (deltaX, deltaY) => ipcRenderer.send('move-window', deltaX, deltaY)
});
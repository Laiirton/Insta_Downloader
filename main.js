const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    autoHideMenuBar: true,
    frame: false,
    transparent: true,
    resizable: false, // Impede o redimensionamento
    fullscreenable: false, // Impede o modo de tela cheia
    backgroundColor: '#00000000', // Fundo transparente
    hasShadow: false
  });

  win.loadFile('index.html');

  // Adicione esta linha para arredondar as bordas no macOS
  if (process.platform === 'darwin') {
    win.setWindowButtonVisibility(false);
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.handle('download-video', async (event, url, savePath, format) => {
  return new Promise((resolve, reject) => {
    const pythonScriptPath = path.join(__dirname, 'downloader.py');
    const pythonProcess = spawn('python', [pythonScriptPath, url, savePath, format], {
      env: { ...process.env, PYTHONIOENCODING: 'utf-8' },
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let output = '';

    pythonProcess.stdout.on('data', (data) => {
      const message = data.toString().trim();
      if (message.startsWith('PROGRESS:')) {
        const progress = parseInt(message.split(':')[1]);
        event.sender.send('download-progress', progress);
      } else {
        output += message + '\n';
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        const successMessage = output.match(/(Áudio|Vídeo) baixado com sucesso: .+\.(mp3|mp4)/);
        if (successMessage) {
          resolve(successMessage[0]);
        } else {
          resolve(output.trim());
        }
      } else {
        reject(`Erro ao fazer o download. Código de saída: ${code}\n${output}`);
      }
    });
  });
});

ipcMain.handle('select-directory', async () => {
  const result = await dialog.showOpenDialog({ properties: ['openDirectory'] });
  return result.filePaths[0];
});

ipcMain.on('close-app', () => {
  app.quit();
});

ipcMain.on('minimize-app', () => {
  BrowserWindow.getFocusedWindow().minimize();
});

ipcMain.on('move-window', (event, deltaX, deltaY) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  const [x, y] = win.getPosition();
  win.setPosition(x + deltaX, y + deltaY);
});
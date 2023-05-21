const path = require('path');
const url = require('url');
const {app, BrowserWindow} = require('electron');


var address = "";
// var python = require("child_process").execFile("backend.exe");
console.log("oooL");

let win;

function saveFile2(url) {
	win.webContents.setWindowOpenHandler(({ url }) => {
		// config.fileProtocol is my custom file protocol
		if (url.startsWith(config.fileProtocol)) {
			return { action: 'allow' };
		}
		// open url in a browser and prevent default
		shell.openExternal(url);
		return { action: 'deny' };
	});
}
function createWindow() {
	win = new BrowserWindow({
		nodeIntegration:true,
		width: 800,
		height: 500,
		icon: __dirname + "/img/icon.png",
		webPreferences: {
			nodeIntegration: false,
			contextIsolation: false,
		}
	});
	win.webContents.openDevTools();
	win.loadURL(url.format({
		pathname: path.join(__dirname, 'index.html'),
		protocol: 'file:',
		slashes: true
	}));

	win.on('closed', () => {
		win = null;
	});
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
	app.quit();
});


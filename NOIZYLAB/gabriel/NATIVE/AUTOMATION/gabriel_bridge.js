/*
 * GABRIEL BRIDGE (JXA)
 * The Native Automation Link for Gabriel System Omega
 *
 * Usage:
 *   osascript -l JavaScript gabriel_bridge.js <function_name> <json_args>
 *
 * Example:
 *   osascript -l JavaScript gabriel_bridge.js launch_app '{"target": "Music"}'
 */

function run(argv) {
     if (argv.length < 2) {
          return JSON.stringify({
               status: "error",
               message: "Insufficient arguments. Usage: gabriel_bridge.js <command> <json_payload>"
          });
     }

     const command = argv[0];
     let payload = {};

     try {
          payload = JSON.parse(argv[1]);
     } catch (e) {
          return JSON.stringify({
               status: "error",
               message: "Invalid JSON payload",
               details: e.toString()
          });
     }

     const app = Application.currentApplication();
     app.includeStandardAdditions = true;

     try {
          switch (command) {
               case "launch_app":
                    return launchApp(payload);
               case "keystroke":
                    return sendKeystroke(payload);
               case "set_volume":
                    return setVolume(payload);
               case "system_info":
                    return getSystemInfo();
               default:
                    return JSON.stringify({
                         status: "error",
                         message: `Unknown command: ${command}`
                    });
          }
     } catch (e) {
          return JSON.stringify({
               status: "error",
               message: "Execution failed",
               details: e.toString()
          });
     }
}

// --- COMMAND HANDLERS ---

function launchApp(data) {
     if (!data.target) throw "Target app not specified";
     const targetApp = Application(data.target);
     targetApp.activate();
     return JSON.stringify({
          status: "success",
          message: `${data.target} activated`
     });
}

function sendKeystroke(data) {
     // Requires accessibility permissions
     const sys = Application("System Events");

     if (data.key) {
          sys.keystroke(data.key);
     } else if (data.code) {
          sys.keyCode(data.code);
     } else {
          throw "No key or code provided";
     }

     return JSON.stringify({
          status: "success",
          message: "Keystroke sent"
     });
}

function setVolume(data) {
     if (data.level === undefined) throw "Volume level (0-100) not specified";
     const app = Application.currentApplication();
     app.includeStandardAdditions = true;
     app.setVolume(null, { outputVolume: data.level });

     return JSON.stringify({
          status: "success",
          level: data.level
     });
}

function getSystemInfo() {
     const app = Application.currentApplication();
     app.includeStandardAdditions = true;
     const info = app.systemInfo();

     return JSON.stringify({
          status: "success",
          computerName: info.computerName,
          osVersion: info.systemVersion,
          cpuSpeed: info.cpuSpeed
     });
}

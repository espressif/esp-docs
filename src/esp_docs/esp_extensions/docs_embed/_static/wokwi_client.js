// Browser bundle of wokwi-client-js
// Use MessagePortTransport for browser communication with Wokwi Simulator


// src/PausePoint.ts
var PausePoint = class {
  constructor(id, params) {
    this.id = id;
    this.params = params;
    this.promise = new Promise((resolve) => {
      this._resolve = resolve;
    });
  }
  resolve(info) {
    this._resolve(info);
  }
};

// src/base64.ts
var b64dict = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
function base64ToByteArray(base64str) {
  if (typeof Buffer !== "undefined") {
    return Uint8Array.from(Buffer.from(base64str, "base64"));
  } else {
    const binaryString = globalThis.atob(base64str);
    return Uint8Array.from(binaryString, (c) => c.charCodeAt(0));
  }
}
function byteArrayToBase64(bytes) {
  if (typeof Buffer !== "undefined") {
    return Buffer.from(bytes.buffer, bytes.byteOffset, bytes.byteLength).toString("base64");
  } else {
    let result = "";
    for (let i = 0; i < bytes.length - 2; i += 3) {
      result += b64dict[bytes[i] >> 2];
      result += b64dict[(bytes[i] & 3) << 4 | bytes[i + 1] >> 4];
      result += b64dict[(bytes[i + 1] & 15) << 2 | bytes[i + 2] >> 6];
      result += b64dict[bytes[i + 2] & 63];
    }
    if (bytes.length % 3 === 1) {
      result += b64dict[bytes[bytes.length - 1] >> 2];
      result += b64dict[(bytes[bytes.length - 1] & 3) << 4];
      result += "==";
    }
    if (bytes.length % 3 === 2) {
      result += b64dict[bytes[bytes.length - 2] >> 2];
      result += b64dict[(bytes[bytes.length - 2] & 3) << 4 | bytes[bytes.length - 1] >> 4];
      result += b64dict[(bytes[bytes.length - 1] & 15) << 2];
      result += "=";
    }
    return result;
  }
}

// src/APIClient.ts
var APIClient = class {
  constructor(transport) {
    this.transport = transport;
    this.lastId = 0;
    this.lastPausePointId = 0;
    this.closed = false;
    this._running = false;
    this._lastNanos = 0;
    this.apiEvents = new EventTarget();
    this.pausePoints = /* @__PURE__ */ new Map();
    this.pendingCommands = /* @__PURE__ */ new Map();
    this.transport.onMessage = (message) => {
      this.processMessage(message);
    };
    this.transport.onClose = (code, reason) => {
      this.handleTransportClose(code, reason);
    };
    this.transport.onError = (error) => {
      this.handleTransportError(error);
    };
    this.connected = this.transport.connect();
  }
  async fileUpload(name, content) {
    if (typeof content === "string") {
      return await this.sendCommand("file:upload", { name, text: content });
    } else {
      return await this.sendCommand("file:upload", {
        name,
        binary: byteArrayToBase64(content)
      });
    }
  }
  async fileDownload(name) {
    const result = await this.sendCommand("file:download", {
      name
    });
    if (typeof result.text === "string") {
      return result.text;
    } else if (typeof result.binary === "string") {
      return base64ToByteArray(result.binary);
    } else {
      throw new Error("Invalid file download response");
    }
  }
  async simStart(params) {
    this._running = false;
    return await this.sendCommand("sim:start", params);
  }
  async simPause() {
    return await this.sendCommand("sim:pause");
  }
  async simResume(pauseAfter) {
    this._running = true;
    return await this.sendCommand("sim:resume", { pauseAfter });
  }
  async simRestart({ pause } = {}) {
    return await this.sendCommand("sim:restart", { pause });
  }
  async simStatus() {
    return await this.sendCommand("sim:status");
  }
  async serialMonitorListen() {
    return await this.sendCommand("serial-monitor:listen");
  }
  async serialMonitorWrite(bytes) {
    return await this.sendCommand("serial-monitor:write", {
      bytes: Array.from(bytes)
    });
  }
  get pausedPromise() {
    if (!this._running) {
      return Promise.resolve();
    }
    return new Promise((resolve) => {
      this.listen("sim:pause", resolve, { once: true });
    });
  }
  async framebufferRead(partId) {
    return await this.sendCommand("framebuffer:read", {
      id: partId
    });
  }
  async controlSet(partId, control, value) {
    return await this.sendCommand("control:set", {
      part: partId,
      control,
      value
    });
  }
  async pinRead(partId, pin) {
    return await this.sendCommand("pin:read", {
      part: partId,
      pin
    });
  }
  async addPausePoint(params, resume = false) {
    const id = `pp${this.lastPausePointId++}_${params.type}`;
    const commands = [this.sendCommand("pause-point:add", { id, ...params })];
    if (resume && !this._running) {
      commands.push(this.simResume());
      this._running = true;
    }
    const pausePoint = new PausePoint(id, params);
    this.pausePoints.set(id, pausePoint);
    await Promise.all(commands);
    return pausePoint;
  }
  async removePausePoint(pausePoint) {
    if (this.pausePoints.has(pausePoint.id)) {
      this.pausePoints.delete(pausePoint.id);
      await this.sendCommand("pause-point:remove", { id: pausePoint.id });
      return true;
    }
    return false;
  }
  async atNanos(nanos) {
    const pausePoint = await this.addPausePoint({ type: "time-absolute", nanos });
    await pausePoint.promise;
  }
  async delay(nanos) {
    const pausePoint = await this.addPausePoint({ type: "time-relative", nanos }, true);
    await pausePoint.promise;
  }
  async waitForSerialBytes(bytes) {
    if (bytes instanceof Uint8Array) {
      bytes = Array.from(bytes);
    }
    const pausePoint = await this.addPausePoint({ type: "serial-bytes", bytes }, true);
    await pausePoint.promise;
  }
  async sendCommand(command, params) {
    return await new Promise((resolve, reject) => {
      const id = this.lastId++;
      this.pendingCommands.set(id.toString(), [resolve, reject]);
      const message = {
        type: "command",
        command,
        params,
        id: id.toString()
      };
      this.transport.send(message);
    });
  }
  get running() {
    return this._running;
  }
  get lastNanos() {
    return this._lastNanos;
  }
  processMessage(message) {
    switch (message.type) {
      case "error":
        if (this.onError) {
          this.onError(message);
        }
        console.error("API Error:", message.message);
        if (this.pendingCommands.size > 0) {
          const entry = this.pendingCommands.values().next().value;
          if (entry) {
            const [, reject] = entry;
            reject(new Error(message.message));
          }
        }
        break;
      case "hello":
        if (message.protocolVersion !== 1) {
          console.warn("Unsupported Wokwi API protocol version", message.protocolVersion);
        }
        this.onConnected?.(message);
        break;
      case "event":
        this.processEvent(message);
        break;
      case "response":
        this.processResponse(message);
        break;
    }
  }
  processEvent(message) {
    if (message.event === "sim:pause") {
      this._running = false;
      const pausePointId = message.payload.pausePoint;
      const pausePoint = this.pausePoints.get(pausePointId);
      if (pausePoint) {
        pausePoint.resolve(message.payload.pausePointInfo);
        this.pausePoints.delete(pausePointId);
      }
    }
    this._lastNanos = message.nanos;
    this.apiEvents.dispatchEvent(new CustomEvent(message.event, { detail: message }));
  }
  listen(event, listener, options) {
    const callback = (e) => {
      if (e.detail == null) {
        return;
      }
      listener(e.detail);
    };
    this.apiEvents.addEventListener(event, callback, options);
    return () => {
      this.apiEvents.removeEventListener(event, callback, options);
    };
  }
  processResponse(message) {
    const id = message.id ?? "";
    const [resolve, reject] = this.pendingCommands.get(id) ?? [];
    if (resolve && reject) {
      this.pendingCommands.delete(id);
      if (message.error) {
        const { result } = message;
        reject(new Error(`Error ${result.code}: ${result.message}`));
      } else {
        resolve(message.result);
      }
    } else {
      console.error("Unknown response", message);
    }
  }
  close() {
    this.closed = true;
    this.transport.close();
  }
  handleTransportClose(code, reason) {
    if (this.closed) return;
    const target = this.server ?? "transport";
    const msg = `Connection to ${target} closed unexpectedly: code ${code}${reason ? ` (${reason})` : ""}`;
    this.onError?.({ type: "error", message: msg });
  }
  handleTransportError(error) {
    this.onError?.({ type: "error", message: error.message });
  }
};

// src/transport/MessagePortTransport.ts
var MessagePortTransport = class {
  constructor(port) {
    this.onMessage = () => {
    };
    this.port = port;
    this.port.onmessage = (event) => {
      this.onMessage(event.data);
    };
    this.port.start();
  }
  async connect() {
  }
  send(message) {
    this.port.postMessage(message);
  }
  close() {
    try {
      this.port.close();
    } catch {
    }
  }
};
export {
  APIClient,
  MessagePortTransport,
  PausePoint,
  base64ToByteArray,
  byteArrayToBase64
};

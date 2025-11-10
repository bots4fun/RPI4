import { useState } from "react";

export default function Home() {
  const [status, setStatus] = useState("");

  const sendCommand = async (action: string) => {
    try {
      const res = await fetch(`http://localhost:8000/motor/${action}`, {
        method: "POST",
      });
      const data = await res.json();
      setStatus(`Command sent: ${data.action}`);
    } catch (err) {
      setStatus("Error sending command");
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Motor Control</h1>
      <div>
        <button onClick={() => sendCommand("forward")}>⬆️ Forward</button>
        <button onClick={() => sendCommand("backward")}>⬇️ Backward</button>
        <button onClick={() => sendCommand("left")}>⬅️ Left</button>
        <button onClick={() => sendCommand("right")}>➡️ Right</button>
        <button onClick={() => sendCommand("stop")}>⏹ Stop</button>
      </div>
      <p>{status}</p>
    </div>
  );
}

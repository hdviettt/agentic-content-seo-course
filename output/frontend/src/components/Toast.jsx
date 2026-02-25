import { useEffect } from "react";
import "./Toast.css";

export default function Toast({ message, onClose }) {
  useEffect(() => {
    if (!message) return;
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [message, onClose]);

  if (!message) return null;

  return (
    <div className="toast" onClick={onClose}>
      {message}
    </div>
  );
}

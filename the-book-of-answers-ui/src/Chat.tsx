import Particles, { initParticlesEngine } from "@tsparticles/react";
import "./App.scss";
import { useEffect, useState, useRef } from "react";
import { loadFull } from "tsparticles";
import type { Container } from "@tsparticles/engine";

type MessageType = "personal" | "bot" | "loading";
interface Message {
  type: MessageType;
  text: string;
  timestamp: string | null;
}
const fakeMessages: string[] = [
  "Hi there, I'm Fabio and you?",
  "Nice to meet you",
  "How are you?",
  "Not too bad, thanks",
  "What do you do?",
  "That's awesome",
  "Codepen is a nice place to stay",
  "I think you're a nice person",
  "Why do you think that?",
  "Can you explain?",
  "Anyway I've gotta go now",
  "It was a pleasure chat with you",
  "Time to make a new codepen",
  "Bye",
  ":)",
];
const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [messageIndex, setMessageIndex] = useState<number>(0);


  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const minutesRef = useRef<number | null>(null);

  useEffect(() => {
    setTimeout(() => {
      handleFakeMessage();
    }, 100);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const getCurrentTimestamp = (): string | null => {
    const now = new Date();
    const minutes = now.getMinutes();
    if (minutesRef.current !== minutes) {
      minutesRef.current = minutes;
      return `${now.getHours()}:${minutes.toString().padStart(2, "0")}`;
    }
    return null;
  };

  const insertMessage = (msgText: string): void => {
    if (!msgText.trim()) return;

    console.log(msgText);
    const timestamp = getCurrentTimestamp();
    console.log(msgText, timestamp);
    setMessages((prev: Message[]) => [
      ...prev,
      { type: "personal", text: msgText, timestamp },
    ]);
    setInput("");
    setTimeout(() => {
      handleFakeMessage();
    }, 1000 + Math.random() * 2000);
  };

  const handleFakeMessage = (): void => {
    if (input.trim()) return;

    setMessages((prev: Message[]) => [
      ...prev,
      { type: "loading", text: "...", timestamp: null },
    ]);

    setTimeout(() => {
      setMessages((prev: Message[]) => {
        const updated = prev.filter((m) => m.type !== "loading");
        const newMessage: Message = {
          type: "bot",
          text: fakeMessages[messageIndex],
          timestamp: getCurrentTimestamp(),
        };
        return [...updated, newMessage];
      });
      setMessageIndex((i: number) => i + 1);
    }, 1000 + Math.random() * 2000);
  };

  const handleSubmit = (): void => {
    console.log("ss");
    insertMessage(input);
  };

  const handleKeyDown = (e: any): void => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  };


  return (
    <>
      <div className="chat">
        <div className="chat-title">
          <h1>The Book of Answers</h1>
          <h2>The Truth</h2>
          <figure className="avatar">
            <img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/156381/profile/profile-80.jpg" />
          </figure>
        </div>
        <div className="messages">
          <div className="messages-content">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message message-${msg.type}`}>
                {msg.type === "bot" || msg.type === "loading" ? (
                  <figure className="avatar">
                    <img
                      src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/156381/profile/profile-80.jpg"
                      alt="avatar"
                    />
                  </figure>
                ) : null}
                <span>{msg.text}</span>
                {msg.timestamp && (
                  <div className="timestamp">{msg.timestamp}</div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>
        <div className="message-box">
          <textarea
            ref={inputRef}
            className="message-input"
            placeholder="Type message..."
          ></textarea>
          <button
            type="submit"
            className="message-submit"
            onClick={handleSubmit}
          >
            Ask
          </button>
        </div>
      </div>
      <div className="bg"></div>

    </>
  );
};

export default Chat;

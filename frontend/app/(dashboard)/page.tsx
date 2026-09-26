import { ChatPanel } from "@/components/chat-panel";

export default function Home() {
  return (
    <div className="flex flex-1 w-full min-w-0 bg-background font-sans">
      <ChatPanel />
    </div>
  );
}
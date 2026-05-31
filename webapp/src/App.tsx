import { Routes, Route } from "react-router-dom";
import AppLayout from "@/components/layout/AppLayout";
import Chat from "@/pages/chat";
import Dashboard from "@/pages/dashboard";
import Games from "@/pages/games";
import Profile from "@/pages/profile";
import Settings from "@/pages/settings";
import Help from "@/pages/help";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/games" element={<Games />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/help" element={<Help />} />
      </Route>
    </Routes>
  );
}

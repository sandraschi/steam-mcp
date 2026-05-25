import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard", icon: "◉" },
  { to: "/games", label: "Games", icon: "🎮" },
  { to: "/profile", label: "Profile", icon: "👤" },
  { to: "/settings", label: "Settings", icon: "⚙" },
  { to: "/help", label: "Help", icon: "?" },
];

export default function Sidebar() {
  return (
    <nav className="w-48 border-r border-zinc-800 bg-zinc-900 p-3 flex flex-col gap-1">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors ${
              isActive
                ? "bg-blue-600 text-white"
                : "text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200"
            }`
          }
          end={link.to === "/"}
        >
          <span>{link.icon}</span>
          <span>{link.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}

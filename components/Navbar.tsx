"use client";

import React, { useState } from "react";
import Link from "next/link";                    
import { Home, Info, FolderKanban, User, Mail } from "lucide-react";

const Navbar = () => {
  const [hoverLabel, setHoverLabel] = useState("");

  const items = [
    { icon: <Home size={24} />, label: "Home", route: "/" },
    { icon: <Info size={24} />, label: "About", route: "/about"},
    { icon: <Mail size={24} />, label: "Contact", route: "/contact" },
  ];

  return (
    <div className="relative w-full flex flex-col items-center py-8 select-none">

      <div
        className={`absolute -top-1 text-white text-sm font-medium transition-all duration-300 ${
          hoverLabel ? "opacity-100" : "opacity-0"
        }`}
      >
        {hoverLabel}
      </div>

      <div
        className="
          flex items-center gap-6 px-6 py-3 rounded-3xl border border-white/10
          bg-white/5 backdrop-blur-xl
          shadow-[0_0_25px_rgba(255,255,255,0.07)]
          transition-all duration-300
        "
      >
        <img
          src="/logo.svg"
          alt="IETE Logo"
          className="
            w-12 h-12 md:w-14 md:h-14 rounded-2xl object-contain
            border border-white/10 p-2 bg-white/5
            hover:border-white/40 hover:bg-white/10 hover:shadow-[0_0_12px_rgba(255,255,255,0.35)]
            transition-all duration-300
          "
        />

        {items.map((item, index) => (
          <Link key={index} href={item.route}>              {/* 👈 add Link wrapper */}
            <button
              onMouseEnter={() => setHoverLabel(item.label)}
              onMouseLeave={() => setHoverLabel("")}
              className="
                flex items-center justify-center w-14 h-14 rounded-2xl
                border border-white/10 text-white transition-all duration-300
                hover:border-white/40 hover:shadow-[0_0_12px_rgba(255,255,255,0.35)]
                hover:bg-white/10 hover:scale-[1.08]
              "
            >
              {item.icon}
            </button>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Navbar;

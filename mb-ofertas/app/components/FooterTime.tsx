"use client";

import { useEffect, useState } from "react";

const formatter = new Intl.DateTimeFormat("pt-BR", {
  timeZone: "America/Sao_Paulo",
  day: "2-digit",
  month: "2-digit",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  hour12: false,
});

function formatUTC3(now: Date): string {
  return formatter.format(now);
}

export function FooterTime() {
  const [time, setTime] = useState<string>(() => formatUTC3(new Date()));

  useEffect(() => {
    const tick = () => setTime(formatUTC3(new Date()));
    tick();
    const id = setInterval(tick, 60_000);
    return () => clearInterval(id);
  }, []);

  return (
    <>
      Horário (UTC-3): {time}
    </>
  );
}

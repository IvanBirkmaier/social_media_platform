import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const backendUrl = import.meta.env.VITE_BACKEND_URL;

export const websocketServerUrl = import.meta.env.WEBSOCKET_SERVER_URL;

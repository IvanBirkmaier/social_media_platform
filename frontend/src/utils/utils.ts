import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";


export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
/*
export const backendUrl = import.meta.env.VITE_BACKEND_URL;

export const url_microservice_one = import.meta.env.VITE_URL_MICROSERVICE_ONE;
export const url_microservice_two = import.meta.env.VITE_URL_MICROSERVICE_TWO;
export const url_microservice_three = import.meta.env.VITE_URL_MICROSERVICE_THREE;
export const url_microservice_four = import.meta.env.VITE_URL_MICROSERVICE_FOUR;
export const websocketServerUrl = import.meta.env.VITE_WEBSOCKET_SERVER_URL;
*/

// Typdefinitionen erweitern
declare global {
  interface Window {
    _env_: {
      [key: string]: string | undefined;
    };
  }
}

export function getConfigValue(key: string): string | undefined {
  return window._env_ ? window._env_[key] : undefined;
}


export const url_microservice_one = getConfigValue('VITE_URL_MICROSERVICE_ONE');
export const url_microservice_two = getConfigValue('VITE_URL_MICROSERVICE_TWO');
export const url_microservice_three = getConfigValue('VITE_URL_MICROSERVICE_THREE');
export const url_microservice_four = getConfigValue('VITE_URL_MICROSERVICE_FOUR');
export const websocketServerUrl = getConfigValue('VITE_WEBSOCKET_SERVER_URL');
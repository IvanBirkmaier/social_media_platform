import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const backendUrl = import.meta.env.VITE_BACKEND_URL;

export const url_microservice_one = import.meta.env.VITE_URL_MICROSERVICE_ONE;
export const url_microservice_two = import.meta.env.VITE_URL_MICROSERVICE_TWO;
export const url_microservice_three = import.meta.env.VITE_URL_MICROSERVICE_THREE;
export const url_microservice_four = import.meta.env.VITE_URL_MICROSERVICE_FOUR;

export const websocketServerUrl = import.meta.env.VITE_WEBSOCKET_SERVER_URL;

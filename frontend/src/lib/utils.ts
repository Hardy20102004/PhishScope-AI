import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function parseUTCDate(dateString: string | Date): Date {
  if (dateString instanceof Date) return dateString;
  if (!dateString) return new Date();
  return new Date(dateString.endsWith('Z') ? dateString : dateString + 'Z');
}

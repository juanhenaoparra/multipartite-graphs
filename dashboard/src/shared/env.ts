export const API_HOST = import.meta.env.VITE_API_HOST

export function GetEnvString(varName: string): string {
  return import.meta.env[varName] || '';
}


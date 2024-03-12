import { API_HOST } from '@/shared/env';
import axios from 'axios';

export async function GetFlow(id: string): Promise<RawGraph> {
  const response = await axios.get(`${API_HOST}/api/graphs/${id}`);
  return response.data;
}

export async function SaveFlow(flow) {
  return await axios.post(`${API_HOST}/api/upload`, flow).then((response) => {
    return response.data;
  })
}
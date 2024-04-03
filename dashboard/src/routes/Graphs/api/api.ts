import { API_HOST } from '@/shared/env';
import axios from 'axios';

export type GenRandomFlowInput = {
  nodesNumber: number
  graphType?: string
  direction: string
  weighted: boolean
  connected: boolean
  complete: boolean
  probability: number
  degree: number
}

export async function GetFlow(id: string): Promise<Graph> {
  const response = await axios.get(`${API_HOST}/api/graphs/${id}`);
  return response.data;
}

export async function SaveFlow(flow) {
  return await axios.post(`${API_HOST}/api/upload`, flow).then((response) => {
    return response.data;
  })
}

export async function GenRandomFlow(input: GenRandomFlowInput) {
  return await axios.post(`${API_HOST}/api/new`, input).then((response) => {
    return response.data;
  })
}

export async function RunCheckBipartite(graphId: string) {
  return await axios.get(`${API_HOST}/api/bipartite/${graphId}`).then((response) => {
    return response.data;
  })
}
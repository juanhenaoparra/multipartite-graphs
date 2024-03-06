import axios from 'axios';

export async function GetFlow(id: string): Promise<RawGraph> {
  const response = await axios.get(`/api/flow/${id}`);
  return response.data;
}

export async function SaveFlow(flow) {
  return await axios.post('/api/flow', flow).then((response) => {
    return response.data;
  })
}
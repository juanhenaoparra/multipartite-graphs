import axios from 'axios';

export async function GetFlow(id: string): Flow {
  const response = await axios.get(`/api/flow/${id}`);
  return response.data;
}

export async function SaveFlow(flow: Flow) {
  axios.post('/api/flow', flow).then((response) => {
    return response.data;
  })
}
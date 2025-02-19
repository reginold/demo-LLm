import axios, { AxiosHeaders } from 'axios';
import { ModelResponse, ComparisonState } from '../types/index';

const API_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  },
  // Add withCredentials
  withCredentials: true
});

// Add request interceptor for debugging
api.interceptors.request.use(request => {
  // Add CORS headers to the request
  if (request.method?.toUpperCase() === 'OPTIONS') {
    const headers = new AxiosHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Access-Control-Request-Method': 'POST',
      'Access-Control-Request-Headers': 'content-type'
    });
    request.headers = headers;
  }
  
  console.log('Starting Request:', {
    url: request.url,
    method: request.method,
    headers: request.headers,
    data: request.data
  });
  return request;
});

interface StreamResponse {
  model: string;
  content: string;
  timing?: {
    duration: number;
  };
  error?: string;
}

export const ModelService = {
  compareModels: async (prompt: string, onUpdate: (modelId: string, content: string, timing?: { duration: number }) => void): Promise<void> => {
    try {
      console.log('Comparing models with prompt:', prompt);
      const response = await fetch(`${API_URL}/api/compare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
        credentials: 'include'
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      while (reader) {
        const { value, done } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data: StreamResponse = JSON.parse(line.slice(6));
              if (data.error) {
                throw new Error(data.error);
              }
              if (data.model && data.content) {
                onUpdate(data.model, data.content, data.timing);
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError);
            }
          }
        }
      }
    } catch (error: any) {
      console.error('Model Comparison Error:', error);
      const errorMessage = `Error: ${error.message}`;
      onUpdate('llama3', errorMessage);
      onUpdate('gpt4o', errorMessage);
      onUpdate('llm_jp', errorMessage);
    }
  },

  callLlmJp172b: async (prompt: string): Promise<string> => {
    try {
      console.log('Calling LLM-JP-172B with prompt:', prompt);
      const response = await api.post<ModelResponse>('/api/llm_jp_172b', { prompt });
      return response.data.result;
    } catch (error: any) {
      console.error('LLM-JP-172B Error:', error);
      return `Error: ${error.message}. Server status: ${error.response?.status || 'unreachable'}`;
    }
  },

  callGpt4o: async (prompt: string): Promise<string> => {
    try {
      console.log('Calling GPT-4o with prompt:', prompt);
      const response = await api.post<ModelResponse>('/api/gpt4o', { prompt });
      return response.data.result;
    } catch (error: any) {
      console.error('GPT-4o Error:', error);
      return `Error: ${error.message}. Server status: ${error.response?.status || 'unreachable'}`;
    }
  },

  callLlama3405b: async (prompt: string): Promise<string> => {
    try {
      console.log('Calling Llama3-405B with prompt:', prompt);
      const response = await api.post<ModelResponse>('/api/llama3_405b', { prompt });
      return response.data.result;
    } catch (error: any) {
      console.error('Llama3-405B Error:', error);
      return `Error: ${error.message}. Server status: ${error.response?.status || 'unreachable'}`;
    }
  }
};
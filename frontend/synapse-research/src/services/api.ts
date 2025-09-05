import { Message, IntentClassification, ResearchResult } from '@/types/research';

// Use environment variable, detect production, or fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (window.location.hostname !== 'localhost' ? window.location.origin : 'http://localhost:8000');

interface ChatRequest {
  message: string;
  sessionId?: string;
  history?: Message[];
}

interface ClassifyIntentRequest {
  message: string;
  history?: Message[];
}

interface ResearchRequest {
  query: string;
}

interface ConversationRequest {
  message: string;
  history?: Message[];
}

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API Error: ${response.status}`);
    }

    return response.json();
  }

  async chat(request: ChatRequest): Promise<Message> {
    const response = await this.request<any>('/api/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
    
    // Convert timestamp string to Date object
    return {
      ...response,
      timestamp: new Date(response.timestamp)
    };
  }

  async classifyIntent(request: ClassifyIntentRequest): Promise<IntentClassification> {
    return this.request<IntentClassification>('/api/classify-intent', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async research(request: ResearchRequest): Promise<ResearchResult> {
    return this.request<ResearchResult>('/api/research', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async conversation(request: ConversationRequest): Promise<{ response: string }> {
    return this.request<{ response: string }>('/api/conversation', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request<{ status: string; timestamp: string }>('/health');
  }
}

export const apiService = new ApiService();
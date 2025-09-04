export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  intent?: 'research' | 'conversation';
  sources?: ResearchSource[];
  reasoning?: string;
}

export interface ResearchSource {
  id: string;
  title: string;
  url: string;
  description: string;
  type: 'paper' | 'article' | 'website';
  metadata?: {
    authors?: string[];
    publishedDate?: string;
    journal?: string;
    doi?: string;
  };
}

export interface IntentClassification {
  intent: 'research' | 'conversation';
  confidence: number;
  reasoning: string;
  optimizedQuery?: string;
}

export interface ResearchResult {
  query: string;
  summary: string;
  sources: ResearchSource[];
  topics: string[];
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export interface FlowState {
  currentMessage: string;
  messageHistory: Message[];
  researchQuery?: string;
  userIntent?: IntentClassification;
  searchResults?: ResearchResult;
  isProcessing: boolean;
  processingType?: 'classification' | 'research' | 'conversation';
}
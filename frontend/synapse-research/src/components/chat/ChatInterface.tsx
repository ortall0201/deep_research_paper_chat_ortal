import React, { useState, useRef, useEffect } from 'react';
import { Message, ChatSession, FlowState, IntentClassification, ResearchResult } from '@/types/research';
import { ChatHeader } from './ChatHeader';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { WelcomeScreen } from './WelcomeScreen';
import { ScrollArea } from '@/components/ui/scroll-area';
import { useToast } from '@/hooks/use-toast';
import { apiService } from '@/services/api';

export const ChatInterface: React.FC = () => {
  const [session, setSession] = useState<ChatSession>({
    id: 'default',
    title: 'Research Session',
    messages: [],
    createdAt: new Date(),
    updatedAt: new Date()
  });
  
  const [flowState, setFlowState] = useState<FlowState>({
    currentMessage: '',
    messageHistory: [],
    isProcessing: false
  });
  
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollContainer = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [session.messages]);

  const handleSendMessage = async (messageContent: string) => {
    // Create user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageContent,
      timestamp: new Date()
    };

    // Add user message to session
    setSession(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      updatedAt: new Date()
    }));

    // Update flow state
    setFlowState(prev => ({
      ...prev,
      currentMessage: messageContent,
      messageHistory: [...prev.messageHistory, userMessage],
      isProcessing: true,
      processingType: 'classification'
    }));

    try {
      // Use the real API to handle the chat
      const assistantMessage = await apiService.chat({
        message: messageContent,
        sessionId: session.id,
        history: session.messages
      });

      // Add assistant message to session
      setSession(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        updatedAt: new Date()
      }));

    } catch (error) {
      console.error('Error processing message:', error);
      toast({
        title: "Error",
        description: "Something went wrong while processing your message. Please try again.",
        variant: "destructive",
      });
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I apologize, but I encountered an error while processing your request. Please try again.",
        timestamp: new Date()
      };
      
      setSession(prev => ({
        ...prev,
        messages: [...prev.messages, errorMessage]
      }));
    } finally {
      // Reset processing state
      setFlowState(prev => ({
        ...prev,
        isProcessing: false,
        processingType: undefined
      }));
    }
  };

  const handleNewSession = () => {
    setSession({
      id: Date.now().toString(),
      title: 'Research Session',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date()
    });
    
    setFlowState({
      currentMessage: '',
      messageHistory: [],
      isProcessing: false
    });
  };

  const handleExampleClick = (example: string) => {
    handleSendMessage(example);
  };

  const showWelcome = session.messages.length === 0;

  return (
    <div className="flex flex-col h-screen bg-chat-background">
      <ChatHeader 
        session={session}
        onNewSession={handleNewSession}
      />
      
      <div className="flex-1 flex flex-col min-h-0">
        {showWelcome ? (
          <WelcomeScreen onExampleClick={handleExampleClick} />
        ) : (
          <ScrollArea ref={scrollAreaRef} className="flex-1 p-4">
            <div className="max-w-4xl mx-auto space-y-6">
              {session.messages.map((message, index) => (
                <ChatMessage 
                  key={message.id}
                  message={message}
                  isLast={index === session.messages.length - 1}
                />
              ))}
            </div>
          </ScrollArea>
        )}
        
        <ChatInput
          onSendMessage={handleSendMessage}
          isProcessing={flowState.isProcessing}
          processingType={flowState.processingType}
          placeholder={showWelcome 
            ? "Ask me about research topics or start a conversation..." 
            : "Continue the conversation..."
          }
        />
      </div>
    </div>
  );
};
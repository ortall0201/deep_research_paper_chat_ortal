import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Send, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isProcessing?: boolean;
  processingType?: 'classification' | 'research' | 'conversation';
  placeholder?: string;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  isProcessing = false,
  processingType,
  placeholder = "Ask me anything about research topics..."
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isProcessing) {
      onSendMessage(message.trim());
      setMessage('');
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
  };

  const getProcessingText = () => {
    switch (processingType) {
      case 'classification':
        return 'Analyzing intent...';
      case 'research':
        return 'Researching...';
      case 'conversation':
        return 'Thinking...';
      default:
        return 'Processing...';
    }
  };

  return (
    <div className="border-t border-border bg-card/50 backdrop-blur-sm p-4">
      <form onSubmit={handleSubmit} className="flex gap-3 items-end max-w-4xl mx-auto">
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={handleTextareaChange}
            onKeyPress={handleKeyPress}
            placeholder={placeholder}
            disabled={isProcessing}
            className={cn(
              "min-h-[44px] max-h-[120px] resize-none pr-12",
              "border-border focus:border-primary/50",
              "transition-all duration-200",
              isProcessing && "opacity-50 cursor-not-allowed"
            )}
            rows={1}
          />
          
          {isProcessing && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2">
              <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
            </div>
          )}
        </div>
        
        <Button
          type="submit"
          size="sm"
          disabled={!message.trim() || isProcessing}
          className={cn(
            "h-11 px-4 flex-shrink-0",
            "bg-gradient-primary hover:opacity-90",
            "transition-all duration-200",
            "disabled:opacity-50 disabled:cursor-not-allowed"
          )}
        >
          {isProcessing ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
          <span className="sr-only">Send message</span>
        </Button>
      </form>
      
      {/* Processing indicator */}
      {isProcessing && (
        <div className="flex items-center justify-center mt-3">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse [animation-delay:0.2s]" />
              <div className="w-2 h-2 bg-primary rounded-full animate-pulse [animation-delay:0.4s]" />
            </div>
            <span>{getProcessingText()}</span>
          </div>
        </div>
      )}
    </div>
  );
};
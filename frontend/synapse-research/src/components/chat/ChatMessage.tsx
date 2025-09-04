import React from 'react';
import { Message } from '@/types/research';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { ExternalLink, Brain, MessageCircle, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: Message;
  isLast?: boolean;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, isLast }) => {
  const isUser = message.role === 'user';
  const hasResearch = message.intent === 'research' && message.sources && message.sources.length > 0;

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const renderContent = () => {
    if (isUser) {
      return (
        <div className="max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl">
          <p className="text-sm sm:text-base">{message.content}</p>
        </div>
      );
    }

    // Assistant message with potential research content
    return (
      <div className="max-w-2xl space-y-4">
        {/* Intent indicator */}
        {message.intent && (
          <div className="flex items-center gap-2 mb-2">
            {message.intent === 'research' ? (
              <Badge variant="secondary" className="research-indicator">
                <Brain className="h-3 w-3 mr-1" />
                Research Mode
              </Badge>
            ) : (
              <Badge variant="secondary" className="conversation-indicator">
                <MessageCircle className="h-3 w-3 mr-1" />
                Conversation
              </Badge>
            )}
          </div>
        )}

        {/* Main content */}
        <div className="prose prose-sm max-w-none">
          <p className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>
        </div>

        {/* Research sources */}
        {hasResearch && (
          <Card className="p-4 bg-research-accent border-research-border">
            <h4 className="font-semibold text-sm mb-3 text-research">
              Sources ({message.sources!.length})
            </h4>
            <div className="space-y-2">
              {message.sources!.map((source, index) => (
                <div key={source.id} className="flex items-start gap-2">
                  <span className="text-xs text-muted-foreground font-mono">
                    [{index + 1}]
                  </span>
                  <div className="flex-1 min-w-0">
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="research-citation text-sm font-medium hover:underline"
                    >
                      {source.title}
                      <ExternalLink className="inline h-3 w-3 ml-1" />
                    </a>
                    {source.description && (
                      <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                        {source.description}
                      </p>
                    )}
                    {source.metadata?.authors && (
                      <p className="text-xs text-muted-foreground mt-1">
                        Authors: {source.metadata.authors.join(', ')}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}
      </div>
    );
  };

  return (
    <div className={cn(
      "flex w-full",
      isUser ? "justify-end" : "justify-start"
    )}>
      <div className={cn(
        "flex gap-3 max-w-full",
        isUser ? "flex-row-reverse" : "flex-row"
      )}>
        {/* Avatar */}
        <div className={cn(
          "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold",
          isUser 
            ? "bg-chat-user text-chat-user-foreground" 
            : "bg-chat-assistant text-chat-assistant-foreground border border-border"
        )}>
          {isUser ? "U" : "AI"}
        </div>

        {/* Message content */}
        <div className={cn(
          "flex flex-col gap-1",
          isUser ? "items-end" : "items-start"
        )}>
          <div className={cn(
            "px-4 py-3 rounded-2xl",
            isUser 
              ? "chat-bubble-user" 
              : "chat-bubble-assistant"
          )}>
            {renderContent()}
          </div>
          
          {/* Timestamp */}
          <div className="flex items-center gap-1 px-2">
            <Clock className="h-3 w-3 text-muted-foreground" />
            <span className="text-xs text-muted-foreground">
              {formatTime(message.timestamp)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
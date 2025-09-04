import React from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Brain, MessageSquare, RotateCcw, Settings } from 'lucide-react';
import { ChatSession } from '@/types/research';

interface ChatHeaderProps {
  session?: ChatSession;
  onNewSession: () => void;
  onSettings?: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({
  session,
  onNewSession,
  onSettings
}) => {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="flex items-center justify-between p-4 max-w-4xl mx-auto">
        {/* Logo and Title */}
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-hero">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg gradient-text">
              Research Assistant
            </h1>
            <p className="text-sm text-muted-foreground">
              Intelligent research & conversation
            </p>
          </div>
        </div>

        {/* Session Info and Actions */}
        <div className="flex items-center gap-2">
          {session && session.messages.length > 0 && (
            <Badge variant="outline" className="hidden sm:flex">
              <MessageSquare className="h-3 w-3 mr-1" />
              {session.messages.length} messages
            </Badge>
          )}
          
          <Button
            variant="outline"
            size="sm"
            onClick={onNewSession}
            className="flex items-center gap-2"
          >
            <RotateCcw className="h-4 w-4" />
            <span className="hidden sm:inline">New Session</span>
          </Button>
          
          {onSettings && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onSettings}
            >
              <Settings className="h-4 w-4" />
              <span className="sr-only">Settings</span>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};
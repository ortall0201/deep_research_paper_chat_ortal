import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Brain, Search, MessageCircle, Zap, ArrowRight } from 'lucide-react';

interface WelcomeScreenProps {
  onExampleClick: (example: string) => void;
}

const examples = [
  {
    category: 'Research',
    icon: Search,
    items: [
      "What are the latest developments in quantum computing?",
      "Research papers on climate change mitigation strategies",
      "Studies about AI impact on healthcare outcomes",
      "Recent findings in renewable energy efficiency"
    ]
  },
  {
    category: 'Analysis',
    icon: Brain,
    items: [
      "Compare different machine learning approaches",
      "Analyze trends in sustainable technology adoption",
      "What are the ethical implications of gene editing?",
      "Economic impact of automation on employment"
    ]
  }
];

export const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onExampleClick }) => {
  return (
    <div className="flex-1 flex items-center justify-center p-6">
      <div className="max-w-3xl mx-auto text-center space-y-8">
        {/* Hero Section */}
        <div className="space-y-4">
          <div className="flex justify-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-hero flex items-center justify-center shadow-lg">
              <Brain className="h-8 w-8 text-white" />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold gradient-text">
            Intelligent Research Assistant
          </h1>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            I analyze your queries to provide either comprehensive research with academic sources 
            or engaging conversational responses. Ask me anything!
          </p>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card className="p-4 text-center border-research-border/50 hover:border-research-border transition-colors">
            <Search className="h-8 w-8 text-research mx-auto mb-2" />
            <h3 className="font-semibold text-sm">Academic Research</h3>
            <p className="text-xs text-muted-foreground mt-1">
              Searches scholarly papers and databases
            </p>
          </Card>
          
          <Card className="p-4 text-center border-conversation-border/50 hover:border-conversation-border transition-colors">
            <MessageCircle className="h-8 w-8 text-conversation mx-auto mb-2" />
            <h3 className="font-semibold text-sm">Smart Conversation</h3>
            <p className="text-xs text-muted-foreground mt-1">
              Context-aware dialogue and explanations
            </p>
          </Card>
          
          <Card className="p-4 text-center border-primary/50 hover:border-primary transition-colors">
            <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
            <h3 className="font-semibold text-sm">Intent Classification</h3>
            <p className="text-xs text-muted-foreground mt-1">
              Automatically routes to best response mode
            </p>
          </Card>
        </div>

        {/* Example Queries */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {examples.map((category) => (
            <Card key={category.category} className="p-6 text-left">
              <div className="flex items-center gap-2 mb-4">
                <category.icon className="h-5 w-5 text-primary" />
                <h3 className="font-semibold">{category.category} Examples</h3>
              </div>
              
              <div className="space-y-2">
                {category.items.map((example, index) => (
                  <Button
                    key={index}
                    variant="ghost"
                    size="sm"
                    onClick={() => onExampleClick(example)}
                    className="w-full justify-between text-left h-auto p-3 text-sm text-muted-foreground hover:text-foreground hover:bg-muted/50"
                  >
                    <span className="text-left">{example}</span>
                    <ArrowRight className="h-4 w-4 flex-shrink-0 ml-2 opacity-50 group-hover:opacity-100" />
                  </Button>
                ))}
              </div>
            </Card>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            Ready to start? Type your question below or click any example above.
          </p>
        </div>
      </div>
    </div>
  );
};
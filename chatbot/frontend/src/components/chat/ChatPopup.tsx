import { useState, useRef, useEffect } from "react";
import { X, Bot } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ChatMessageComponent } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ChatMessage, sendMessageStream, generateId } from "@/services/chatService";
import { cn } from "@/lib/utils";

interface ChatPopupProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ChatPopup = ({ isOpen, onClose }: ChatPopupProps) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: generateId(),
      role: 'assistant',
      content: 'Olá! Sou o assistente virtual. Como posso ajudá-lo hoje?',
      timestamp: new Date(),
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  const handleSend = async (content: string) => {
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingContent('');

    // Build conversation history for context
    const conversationHistory = [...messages, userMessage].map(m => ({
      role: m.role,
      content: m.content,
    }));

    let assistantContent = '';

    await sendMessageStream(
      conversationHistory,
      (chunk) => {
        assistantContent += chunk;
        setStreamingContent(assistantContent);
      },
      () => {
        const assistantMessage: ChatMessage = {
          id: generateId(),
          role: 'assistant',
          content: assistantContent,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
        setStreamingContent('');
        setIsLoading(false);
      },
      (error) => {
        console.error('Error sending message:', error);
        const errorMessage: ChatMessage = {
          id: generateId(),
          role: 'assistant',
          content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Verifique sua conexão',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessage]);
        setStreamingContent('');
        setIsLoading(false);
      }
    );
  };

  return (
    <div className={cn(
      "fixed bottom-24 right-6 w-[380px] max-w-[calc(100vw-3rem)] h-[500px] max-h-[calc(100vh-8rem)]",
      "bg-card rounded-2xl shadow-2xl border border-border flex flex-col overflow-hidden",
      "transition-all duration-300 ease-out origin-bottom-right",
      isOpen ? "scale-100 opacity-100" : "scale-95 opacity-0 pointer-events-none"
    )}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-primary text-primary-foreground">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-primary-foreground/20 flex items-center justify-center">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-sm">Assistente Virtual</h3>
            <p className="text-xs opacity-80">Apita Cidadão</p>
          </div>
        </div>
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={onClose}
          className="hover:bg-primary-foreground/20 text-primary-foreground"
        >
          <X className="w-5 h-5" />
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto bg-background">
        {messages.map((message) => (
          <ChatMessageComponent key={message.id} message={message} />
        ))}
        {/* Streaming message */}
        {streamingContent && (
          <ChatMessageComponent 
            message={{
              id: 'streaming',
              role: 'assistant',
              content: streamingContent,
              timestamp: new Date(),
            }} 
          />
        )}
        {isLoading && !streamingContent && (
          <div className="flex gap-3 p-3">
            <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center">
              <Bot className="w-4 h-4 text-muted-foreground" />
            </div>
            <div className="bg-muted rounded-2xl rounded-bl-md px-4 py-2.5">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-muted-foreground/50 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-muted-foreground/50 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-muted-foreground/50 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
};

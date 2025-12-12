import { cn } from "@/lib/utils";
import { ChatMessage as ChatMessageType } from "@/services/mockChatService";
import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessageComponent = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={cn(
      "flex gap-3 p-3",
      isUser ? "flex-row-reverse" : "flex-row"
    )}>
      <div className={cn(
        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
        isUser ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
      )}>
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>
      
      <div className={cn(
        "max-w-[80%] rounded-2xl px-4 py-2.5 text-sm",
        isUser 
          ? "bg-primary text-primary-foreground rounded-br-md" 
          : "bg-muted text-foreground rounded-bl-md prose prose-sm prose-neutral dark:prose-invert max-w-none"
      )}>
        {isUser ? (
          message.content
        ) : (
          <ReactMarkdown 
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              ul: ({ children }) => <ul className="list-disc list-inside mb-2">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside mb-2">{children}</ol>,
              h1: ({ children }) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
              h2: ({ children }) => <h2 className="text-base font-bold mb-2">{children}</h2>,
              h3: ({ children }) => <h3 className="text-sm font-bold mb-1">{children}</h3>,
              code: ({ className, children, ...props }) => {
                const isInline = !className;
                return isInline ? (
                  <code className="bg-background/50 px-1 py-0.5 rounded text-xs" {...props}>{children}</code>
                ) : (
                  <code className="block bg-background/50 p-2 rounded text-xs overflow-x-auto my-2" {...props}>{children}</code>
                );
              },
              pre: ({ children }) => <pre className="bg-background/50 p-2 rounded overflow-x-auto my-2">{children}</pre>,
              a: ({ children, href }) => <a href={href} className="text-primary underline" target="_blank" rel="noopener noreferrer">{children}</a>,
            }}
          >
            {message.content.replace(/\\n/g, '\n').replace(/\\\\n/g, '\n')}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
};

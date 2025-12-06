import { FloatingChatButton } from "@/components/chat/FloatingChatButton";
import { MessageCircle } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-primary text-primary-foreground py-6">
        <div className="container mx-auto px-4">
          <h1 className="text-2xl md:text-3xl font-bold">Apita Cidadão</h1>
        </div>
      </header>

      {/* Main Content - Empty with icon */}
      <main className="flex-1 flex flex-col items-center justify-center min-h-[calc(100vh-88px)]">
        <MessageCircle className="w-24 h-24 text-muted-foreground/30" />
        <p className="text-muted-foreground mt-4">Clique no ícone de chat para começar</p>
      </main>

      {/* Floating Chat */}
      <FloatingChatButton />
    </div>
  );
};

export default Index;

export interface Message {
  content: string;
  isUser: boolean;
}

export interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export interface FileSidebarProps {
  onUpload: () => void; // Add this prop type definition
}


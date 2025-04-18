export interface Message {
  content: string;
  isUser: boolean;
}

export interface MessageListProps {
  messages: Message[];
}

export interface FileSidebarProps {
  onUpload: () => void; // Add this prop type definition
}

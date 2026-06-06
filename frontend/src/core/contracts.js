export const MessageRole = {
  USER: "user",
  AI: "ai",
};

export function createMessage(role, text) {
  return {
    role,
    text,
  };
}
export default function Sidebar({
  conversations,
  currentChatId,
  setCurrentChatId,
  createNewChat,
  deleteChat,
  editingChatId,
  editingTitle,
  setEditingTitle,
  startRename,
  saveRename,
  cancelRename,
}) {
  return (
    <div className="w-64 h-full border-r border-zinc-800 flex flex-col">

      <div className="p-3 border-b border-zinc-800">
        <button
          onClick={createNewChat}
          className="w-full bg-white text-black py-2 rounded-lg text-sm font-medium"
        >
           New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">

        {conversations.length === 0 && (
          <div className="text-xs text-zinc-500 p-2">
            No conversations yet
          </div>
        )}

        {conversations.map((chat) => (
          <div
            key={chat.id}
            onClick={() => setCurrentChatId(chat.id)}
            className={`group flex items-center justify-between p-2 rounded cursor-pointer text-sm transition ${
              chat.id === currentChatId
                ? "bg-zinc-800"
                : "hover:bg-zinc-900"
            }`}
          >

            <div className="flex-1 truncate">
              {editingChatId === chat.id ? (
                <input
                  autoFocus
                  value={editingTitle}
                  onChange={(e) => setEditingTitle(e.target.value)}
                  onBlur={saveRename}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") saveRename();
                    if (e.key === "Escape") cancelRename();
                  }}
                  className="w-full bg-zinc-900 text-white px-2 py-1 rounded outline-none"
                />
              ) : (
                chat.title
              )}
            </div>

            {editingChatId !== chat.id && (
              <div className="hidden group-hover:flex gap-2 ml-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    startRename(chat);
                  }}
                >
                  ✏
                </button>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteChat(chat.id);
                  }}
                >
                  🗑
                </button>
              </div>
            )}

          </div>
        ))}
      </div>
    </div>
  );
}
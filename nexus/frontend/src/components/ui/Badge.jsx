export default function Badge({
  children,
  className = "",
}) {
  return (
    <span
      className={`
        inline-flex
        items-center
        rounded-full
        px-3
        py-1
        text-xs
        font-medium
        bg-blue-500/10
        text-blue-400
        border
        border-blue-500/20
        ${className}
      `}
    >
      {children}
    </span>
  );
}
export default function Input({
  className = "",
  ...props
}) {
  return (
    <input
      className={`
        w-full
        bg-zinc-900
        border
        border-zinc-800
        rounded-xl
        px-4
        py-3
        text-white
        outline-none
        focus:border-blue-500
        transition-all
        duration-200
        ${className}
      `}
      {...props}
    />
  );
}
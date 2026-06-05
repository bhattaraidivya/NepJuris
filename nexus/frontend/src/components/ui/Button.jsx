import { buttons } from "../../design/buttons";

export default function Button({
  children,
  variant = "primary",
  className = "",
  ...props
}) {
  return (
    <button
      className={`${buttons[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
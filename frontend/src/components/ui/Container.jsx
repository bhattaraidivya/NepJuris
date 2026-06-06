import { layout } from "../../design/layout";

export default function Container({
  children,
  className = "",
}) {
  return (
    <div
      className={`${layout.container} ${className}`}
    >
      {children}
    </div>
  );
}
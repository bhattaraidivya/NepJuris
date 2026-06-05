import { spacing } from "../../design/spacing";

export default function Section({
  children,
  className = "",
}) {
  return (
    <section
      className={`${spacing.section} ${className}`}
    >
      {children}
    </section>
  );
}
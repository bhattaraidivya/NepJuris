export default function Card({ title, description }) {
  return (
    <div className="p-5 rounded-xl border border-zinc-800 bg-zinc-900/40">
      <h4 className="text-lg font-semibold">{title}</h4>

      <p className="text-sm text-zinc-400 mt-2">
        {description}
      </p>
    </div>
  );
}
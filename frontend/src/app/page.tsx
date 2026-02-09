import ReplyForm from "../components/ReplyForm";

export default function Home() {
  return (
    <main style={{ maxWidth: "800px", margin: "0 auto", padding: "24px" }}>
      <h1>上司案件・落とし所AIエージェント</h1>
      <p>「今日中に」を今日中にしないAI</p>
      <div style={{ marginTop: "32px" }}>
        <ReplyForm />
      </div>
    </main>
  );
}

import Navbar from "../components/layout/Navbar";
import Hero from "../components/home/Hero";
import Workflow from "../components/home/Workflow";
import Transition from "../components/home/CorpusPreview";
import Features from "../components/home/Features";
import Trust from "../components/home/Trust";
import Footer from "../components/layout/Footer";
import Message from "../components/chat/Message";
import CorpusPreview from "../components/home/CorpusPreview";


export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <Navbar />
      <Hero />
      <Workflow />
      <CorpusPreview />
      <Features />
      <Trust />
      <Footer />
      <Message />

    </div>
  );
}
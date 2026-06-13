import Navbar from "../components/layout/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import HowItWorks from "../components/HowItWorks";
import CTA from "../components/CTA";
import Footer from "../components/layout/Footer";
function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <Features /> 
      <HowItWorks />
      <CTA />
      <Footer / >
    </>
  );
}

export default Home;
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import FeatureCard from "../components/FeatureCard";
import HowItWorks from "../components/HowItWorks";
import Footer from "../components/Footer";

function Landing() {
  return (
    <>
      <Navbar />

      <Hero />

      <section className="features">
        <FeatureCard
          title="AI Tutor"
          description="Ask academic questions using NCERT-powered AI."
        />

        <FeatureCard
          title="Performance Analytics"
          description="Track strengths, weaknesses and learning trends."
        />

        <FeatureCard
          title="Study Planner"
          description="Receive personalized weekly study plans."
        />

        <FeatureCard
          title="Personalized Feedback"
          description="Get AI-generated feedback and improvement suggestions."
        />
      </section>

      <HowItWorks />

      <Footer />
    </>
  );
}

export default Landing;

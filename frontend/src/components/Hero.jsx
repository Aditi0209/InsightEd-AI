import { Link } from "react-router-dom";

function Hero() {

    return (

        <section className="hero">

            <h1>
                Learn Smarter with AI
            </h1>

            <p>
                Personalized tutoring, performance analytics,
                AI-generated study plans and intelligent academic
                guidance — all in one platform.
            </p>

            <Link to="/login">
            <button>
                Get Started
            </button>
            </Link>

        </section>

    );

}

export default Hero;
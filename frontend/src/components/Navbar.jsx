import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        Academic Mentor AI
      </div>

      <Link to="/login">

    <button className="login-btn">

        Login

    </button>

</Link>
    </nav>
  );
}

export default Navbar;
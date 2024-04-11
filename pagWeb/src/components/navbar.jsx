import { Link } from 'react-router-dom';
import './navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-links">
        <Link to="/">Engine</Link>
        <Link to="/glossary">Glossary</Link>
        <Link to="/history">History</Link>
      </div>
      <div className="title">Concrete is Meaningful - Abstract Finder</div>
    </nav>
  );
}

export default Navbar;

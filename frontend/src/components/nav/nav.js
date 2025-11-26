import NavItem from '../nav_item/nav_item';
import "./nav.css";

function nav() {
    return (
        <nav className="nav">
            <ul className="nav-list">
                <NavItem href="/" >Home</NavItem>
                <NavItem href="/about" >About</NavItem>
                <NavItem href="/services" >Services</NavItem>
                <NavItem href="/contact" >Contact</NavItem>
                <NavItem href="/login" >Login</NavItem>
                <NavItem href="/register" >Register</NavItem>
            </ul>
        </nav>
    );
}

export default nav;
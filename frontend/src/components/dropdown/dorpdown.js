import DropdownItem from './dropdown_item/dropdown_item';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

function Dropdown() {
    return (
        <div className="dropdown">
            <button className="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false"><i className="bi bi-list"></i>Menu</button>
            <ul className="dropdown-menu">
                <DropdownItem href="/about">About</DropdownItem>
                <DropdownItem href="/services">Services</DropdownItem>
                <DropdownItem href="/contact">Contact</DropdownItem>
                <DropdownItem href="/login">Login</DropdownItem>
                <DropdownItem href="/register">Register</DropdownItem>
            </ul>
        </div>
    );
}

export default Dropdown;
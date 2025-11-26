import { Link } from 'react-router-dom';
import "./nav_item.css";

function NavItem(props) {
    return (
        <li className="nav-item-list">
            <Link className="nav-item" to={props.href}>{props.children}</Link>
        </li>
    );
}

export default NavItem;

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

function DropdownItem(props) {
    return (
        <li>
            <a className="dropdown-item" href={props.href}>{props.children}</a>
        </li>
    );
}

export default DropdownItem;
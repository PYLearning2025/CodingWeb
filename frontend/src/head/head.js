import Nav from '../components/nav/nav';
import Logo from './logo/logo';
import Dropdown from '../components/dropdown/dorpdown';
import "./head.css";

function Head() {
    return (
        <div className="head">
            <Logo />
            <Nav />
            <Dropdown />
        </div>
    );
}

export default Head;
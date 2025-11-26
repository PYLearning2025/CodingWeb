import "./logo.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap-icons/font/bootstrap-icons.css";

function Logo() {
    return (
        <div className="logo">
            <h1 className="logo-text"><a href="/"><i className="bi bi-code-slash"></i>程式設計</a></h1>
        </div>
    );
}

export default Logo;
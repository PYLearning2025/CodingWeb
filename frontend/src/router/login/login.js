import React, { useState } from 'react';
import api from '../../fetch/fetch';
import './login.css';

function Login() {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        if (error) setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!formData.username || !formData.password) {
            setError('請輸入帳號與密碼');
            return;
        }

        setLoading(true);

        try {
            // 呼叫後端 /login API
            const response = await api.post('/login', formData);
            
            console.log('登入成功:', response);
            alert('登入成功！');
            // TODO: 處理 token 儲存與轉址
            
        } catch (err) {
            console.error('登入失敗:', err);
            setError(err.message || '登入失敗，請稍後再試');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6 col-lg-4">
                    <div className="card shadow-sm">
                        <div className="card-body p-4">
                            <h3 className="card-title text-center mb-4">會員登入</h3>
                            
                            {error && <div className="alert alert-danger" role="alert">{error}</div>}
                            
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3 text-start">
                                    <label htmlFor="username" className="form-label">帳號</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="username"
                                        name="username"
                                        value={formData.username}
                                        onChange={handleChange}
                                        placeholder="請輸入帳號"
                                        disabled={loading}
                                    />
                                </div>
                                
                                <div className="mb-4 text-start">
                                    <label htmlFor="password" className="form-label">密碼</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        id="password"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleChange}
                                        placeholder="請輸入密碼"
                                        disabled={loading}
                                    />
                                </div>

                                <button 
                                    type="submit" 
                                    className="btn btn-primary w-100"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <span>
                                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                            登入中...
                                        </span>
                                    ) : '登入'}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;


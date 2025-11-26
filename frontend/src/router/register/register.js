import React, { useState } from 'react';
import api from '../../fetch/fetch';
import './register.css';

function Register() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
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

        // 驗證
        if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
            setError('請填寫所有欄位');
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('兩次密碼輸入不一致');
            return;
        }

        setLoading(true);

        try {
            // 準備送出資料，移除確認密碼欄位
            const { confirmPassword, ...submitData } = formData;
            
            // 呼叫後端 /register API
            const response = await api.post('/register', submitData);
            
            console.log('註冊成功:', response);
            alert('註冊成功！請登入');
            // 這裡可以轉址到登入頁
            // window.location.href = '/login';
            
        } catch (err) {
            console.error('註冊失敗:', err);
            setError(err.message || '註冊失敗，請稍後再試');
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
                            <h3 className="card-title text-center mb-4">會員註冊</h3>
                            
                            {error && <div className="alert alert-danger" role="alert">{error}</div>}
                            
                            <form onSubmit={handleSubmit}>
                                <div className="mb-3 text-start">
                                    <label htmlFor="name" className="form-label">使用者名稱</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="name"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        placeholder="請輸入使用者名稱"
                                        disabled={loading}
                                    />
                                </div>

                                <div className="mb-3 text-start">
                                    <label htmlFor="email" className="form-label">電子信箱</label>
                                    <input
                                        type="email"
                                        className="form-control"
                                        id="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        placeholder="請輸入 Email"
                                        disabled={loading}
                                    />
                                </div>
                                
                                <div className="mb-3 text-start">
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

                                <div className="mb-4 text-start">
                                    <label htmlFor="confirmPassword" className="form-label">確認密碼</label>
                                    <input
                                        type="password"
                                        className="form-control"
                                        id="confirmPassword"
                                        name="confirmPassword"
                                        value={formData.confirmPassword}
                                        onChange={handleChange}
                                        placeholder="請再次輸入密碼"
                                        disabled={loading}
                                    />
                                </div>

                                <button 
                                    type="submit" 
                                    className="btn btn-success w-100"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <span>
                                            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                            註冊中...
                                        </span>
                                    ) : '註冊'}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Register;


/**
 * 獲取後端基礎 URL
 * 注意: 在 Create React App 中，環境變數必須以 REACT_APP_ 開頭才能在前端存取
 * 請確保您的 .env 檔案中有設定 REACT_APP_BACKEND_URL
 */
const BASE_URL = process.env.REACT_APP_BACKEND_URL || process.env.backend_url || "http://localhost:8000";

/**
 * 核心 API 呼叫函數
 * @param {string} endpoint - API路徑 (例如: '/api/login')
 * @param {Object} options - fetch選項 (method, body, headers等)
 * @returns {Promise<any>} - 解析後的 JSON 回應
 */
export const apiFetch = async (endpoint, options = {}) => {
  // 移除開頭的斜線以避免雙重斜線，如果 BASE_URL 結尾沒有斜線
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const url = `${BASE_URL}${cleanEndpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  // 如果有 body 且不是 FormData (通常是 JSON)，則自動轉字串
  if (config.body && !(config.body instanceof FormData) && typeof config.body === 'object') {
    config.body = JSON.stringify(config.body);
  }

  // 如果是 FormData，刪除 Content-Type header讓瀏覽器自動設定 (包含 boundary)
  if (config.body instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  try {
    const response = await fetch(url, config);

    // 嘗試解析 JSON，如果失敗則回傳文字或 null
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      // 建構錯誤訊息物件
      const error = new Error(data?.message || `Request failed with status ${response.status}`);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  } catch (error) {
    console.error('API Call Error:', error);
    throw error;
  }
};

/**
 * RESTful API 通用方法
 */
const api = {
  /**
   * GET 請求
   * @param {string} endpoint 
   * @param {Object} headers 
   */
  get: (endpoint, headers = {}) => apiFetch(endpoint, { method: 'GET', headers }),

  /**
   * POST 請求
   * @param {string} endpoint 
   * @param {Object} body - 請求資料
   * @param {Object} headers 
   */
  post: (endpoint, body, headers = {}) => apiFetch(endpoint, { method: 'POST', body, headers }),

  /**
   * PUT 請求
   * @param {string} endpoint 
   * @param {Object} body - 更新資料
   * @param {Object} headers 
   */
  put: (endpoint, body, headers = {}) => apiFetch(endpoint, { method: 'PUT', body, headers }),

  /**
   * PATCH 請求
   * @param {string} endpoint 
   * @param {Object} body - 部分更新資料
   * @param {Object} headers 
   */
  patch: (endpoint, body, headers = {}) => apiFetch(endpoint, { method: 'PATCH', body, headers }),

  /**
   * DELETE 請求
   * @param {string} endpoint 
   * @param {Object} headers 
   */
  del: (endpoint, headers = {}) => apiFetch(endpoint, { method: 'DELETE', headers }),
};

export default api;

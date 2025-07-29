import axios from 'axios'

// Create axios instance with base configuration
export const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const userApi = {
  getUsers: (skip = 0, limit = 100) =>
    api.get(`/v1/users/?skip=${skip}&limit=${limit}`),
  getUser: (id: number) => api.get(`/v1/users/${id}`),
  createUser: (userData: any) => api.post('/v1/users/', userData),
  updateUser: (id: number, userData: any) => api.put(`/v1/users/${id}`, userData),
  deleteUser: (id: number) => api.delete(`/v1/users/${id}`),
}

export const reportApi = {
  getReports: () => api.get('/v1/reports/'),
  getReport: (id: number) => api.get(`/v1/reports/${id}`),
  createReport: (reportData: any) => api.post('/v1/reports/', reportData),
}

export const downloadApi = {
  getDownloads: () => api.get('/v1/downloads/'),
  downloadFile: (id: number) => api.get(`/v1/downloads/${id}`, { responseType: 'blob' }),
}

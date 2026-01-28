import axios from 'axios';

// Base API URL - Change this to your backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API Service Methods
const apiService = {
  // Upload CSV file
  uploadCSV: (file, type) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    
    return apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Patient APIs
  createPatient: (patientData) => {
    return apiClient.post('/patient', patientData);
  },

  getPatients: (params) => {
    return apiClient.get('/patients', { params });
  },

  getPatientById: (id) => {
    return apiClient.get(`/patient/${id}`);
  },

  updatePatient: (id, patientData) => {
    return apiClient.put(`/patient/${id}`, patientData);
  },

  deletePatient: (id) => {
    return apiClient.delete(`/patient/${id}`);
  },

  // Visit APIs
  createVisit: (visitData) => {
    return apiClient.post('/visit', visitData);
  },

  getVisits: (params) => {
    return apiClient.get('/visits', { params });
  },

  getVisitById: (id) => {
    return apiClient.get(`/visit/${id}`);
  },

  updateVisit: (id, visitData) => {
    return apiClient.put(`/visit/${id}`, visitData);
  },

  deleteVisit: (id) => {
    return apiClient.delete(`/visit/${id}`);
  },

  // Prescription APIs
  createPrescription: (prescriptionData) => {
    return apiClient.post('/prescription', prescriptionData);
  },

  getPrescriptions: (params) => {
    return apiClient.get('/prescriptions', { params });
  },

  getPrescriptionById: (id) => {
    return apiClient.get(`/prescription/${id}`);
  },

  updatePrescription: (id, prescriptionData) => {
    return apiClient.put(`/prescription/${id}`, prescriptionData);
  },

  deletePrescription: (id) => {
    return apiClient.delete(`/prescription/${id}`);
  },

  // Dashboard & Analytics APIs
  getDashboardData: () => {
    return apiClient.get('/dashboard');
  },

  getAnalytics: (params) => {
    return apiClient.get('/analytics', { params });
  },

  // Health check
  healthCheck: () => {
    return apiClient.get('/health');
  },
};

export default apiService;

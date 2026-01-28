import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { FaChartLine, FaUsers, FaHospital, FaPills, FaDownload } from 'react-icons/fa';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState({
    summary: {
      totalPatients: 0,
      totalVisits: 0,
      totalPrescriptions: 0,
      activeCases: 0
    },
    ageDistribution: [],
    visitTrends: [],
    diseaseDistribution: [],
    genderDistribution: []
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/dashboard');
      if (response.data.success) {
        setDashboardData(response.data.data);
      } else {
        // Use mock data if backend is not ready
        loadMockData();
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Use mock data for development
      loadMockData();
    } finally {
      setLoading(false);
    }
  };

  const loadMockData = () => {
    setDashboardData({
      summary: {
        totalPatients: 1248,
        totalVisits: 3567,
        totalPrescriptions: 4892,
        activeCases: 342
      },
      ageDistribution: [
        { ageGroup: '0-18', count: 245 },
        { ageGroup: '19-35', count: 432 },
        { ageGroup: '36-50', count: 387 },
        { ageGroup: '51-65', count: 156 },
        { ageGroup: '65+', count: 28 }
      ],
      visitTrends: [
        { month: 'Jan', visits: 280 },
        { month: 'Feb', visits: 320 },
        { month: 'Mar', visits: 298 },
        { month: 'Apr', visits: 345 },
        { month: 'May', visits: 412 },
        { month: 'Jun', visits: 389 }
      ],
      diseaseDistribution: [
        { disease: 'Diabetes', count: 234 },
        { disease: 'Hypertension', count: 198 },
        { disease: 'Asthma', count: 156 },
        { disease: 'Arthritis', count: 123 },
        { disease: 'Other', count: 345 }
      ],
      genderDistribution: [
        { gender: 'Male', value: 52 },
        { gender: 'Female', value: 45 },
        { gender: 'Other', value: 3 }
      ]
    });
  };

  const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444'];

  const downloadReport = () => {
    alert('Report download feature coming soon!');
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div>
          <h1><FaChartLine /> Analytics Dashboard</h1>
          <p>Real-time healthcare data insights and visualization</p>
        </div>
        <button className="btn btn-success" onClick={downloadReport}>
          <FaDownload /> Download Report
        </button>
      </div>

      {/* Summary Cards */}
      <div className="stats-grid">
        <div className="stat-card" style={{'--card-color': '#2563eb'}}>
          <div className="stat-icon" style={{background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)'}}>
            <FaUsers />
          </div>
          <div className="stat-content">
            <h3>Total Patients</h3>
            <p className="stat-value">{dashboardData.summary.totalPatients.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card" style={{'--card-color': '#10b981'}}>
          <div className="stat-icon" style={{background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'}}>
            <FaHospital />
          </div>
          <div className="stat-content">
            <h3>Total Visits</h3>
            <p className="stat-value">{dashboardData.summary.totalVisits.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card" style={{'--card-color': '#8b5cf6'}}>
          <div className="stat-icon" style={{background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)'}}>
            <FaPills />
          </div>
          <div className="stat-content">
            <h3>Prescriptions</h3>
            <p className="stat-value">{dashboardData.summary.totalPrescriptions.toLocaleString()}</p>
          </div>
        </div>

        <div className="stat-card" style={{'--card-color': '#f59e0b'}}>
          <div className="stat-icon" style={{background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'}}>
            <FaChartLine />
          </div>
          <div className="stat-content">
            <h3>Active Cases</h3>
            <p className="stat-value">{dashboardData.summary.activeCases.toLocaleString()}</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Age Distribution */}
        <div className="chart-card">
          <h2 className="chart-title">Age Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboardData.ageDistribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="ageGroup" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip 
                contentStyle={{
                  background: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Bar dataKey="count" fill="#2563eb" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Visit Trends */}
        <div className="chart-card">
          <h2 className="chart-title">Monthly Visit Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={dashboardData.visitTrends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip 
                contentStyle={{
                  background: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="visits" 
                stroke="#10b981" 
                strokeWidth={3}
                dot={{ fill: '#10b981', r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Disease Distribution */}
        <div className="chart-card">
          <h2 className="chart-title">Common Diagnoses</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboardData.diseaseDistribution} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" stroke="#64748b" />
              <YAxis dataKey="disease" type="category" stroke="#64748b" width={100} />
              <Tooltip 
                contentStyle={{
                  background: 'white',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Bar dataKey="count" fill="#8b5cf6" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Gender Distribution */}
        <div className="chart-card">
          <h2 className="chart-title">Gender Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={dashboardData.genderDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ gender, value }) => `${gender}: ${value}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {dashboardData.genderDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Insights Section */}
      <div className="insights-section">
        <h2 className="section-title">Key Insights</h2>
        <div className="insights-grid">
          <div className="insight-card">
            <h3>Most Common Age Group</h3>
            <p>Patients aged 19-35 represent the largest demographic at 35% of total patients</p>
          </div>
          <div className="insight-card">
            <h3>Visit Growth</h3>
            <p>Monthly visits have increased by 47% over the past 6 months</p>
          </div>
          <div className="insight-card">
            <h3>Primary Diagnoses</h3>
            <p>Diabetes and Hypertension account for 42% of all diagnoses</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

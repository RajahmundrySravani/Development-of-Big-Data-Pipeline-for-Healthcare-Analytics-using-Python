import React from 'react';
import { Link } from 'react-router-dom';
import { FaCloudUploadAlt, FaEdit, FaChartLine } from 'react-icons/fa';
import './Home.css';

const Home = () => {
  const features = [
    {
      icon: <FaCloudUploadAlt />,
      title: 'Batch Data Upload',
      description: 'Upload CSV files for Patients, Visits, and Prescriptions',
      link: '/upload',
      color: '#3b82f6'
    },
    {
      icon: <FaEdit />,
      title: 'Real-time Data Entry',
      description: 'Enter patient, visit, and prescription data through forms',
      link: '/data-entry',
      color: '#10b981'
    },
    {
      icon: <FaChartLine />,
      title: 'Analytics Dashboard',
      description: 'Visualize insights with interactive charts and reports',
      link: '/dashboard',
      color: '#8b5cf6'
    }
  ];

  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Healthcare Data Analytics System
          </h1>
          <p className="hero-subtitle">
            Professional data management platform for healthcare analytics powered by AWS, PySpark, and MongoDB
          </p>
          <div className="hero-buttons">
            <Link to="/upload" className="btn btn-primary">
              Get Started
            </Link>
            <Link to="/dashboard" className="btn btn-secondary">
              View Dashboard
            </Link>
          </div>
        </div>
        <div className="hero-animation">
          <div className="pulse-circle"></div>
          <div className="pulse-circle delay-1"></div>
          <div className="pulse-circle delay-2"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">Core Features</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <Link to={feature.link} key={index} className="feature-card" style={{'--card-color': feature.color}}>
              <div className="feature-icon" style={{color: feature.color}}>
                {feature.icon}
              </div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
              <span className="feature-arrow">→</span>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Start Analyzing Healthcare Data?</h2>
          <p>Upload your data or explore our interactive dashboard</p>
          <Link to="/upload" className="btn btn-success">
            Upload Data Now
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;

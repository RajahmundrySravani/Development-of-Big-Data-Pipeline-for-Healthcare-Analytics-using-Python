import React, { useState } from 'react';
import { FaCloudUploadAlt, FaFileUpload, FaCheckCircle, FaTimesCircle } from 'react-icons/fa';
import axios from 'axios';
import './Upload.css';

const Upload = () => {
  const [selectedFiles, setSelectedFiles] = useState({
    patients: null,
    visits: null,
    prescriptions: null
  });

  const [uploadStatus, setUploadStatus] = useState({
    patients: '',
    visits: '',
    prescriptions: ''
  });

  const [loading, setLoading] = useState({
    patients: false,
    visits: false,
    prescriptions: false
  });

  const handleFileSelect = (e, type) => {
    const file = e.target.files[0];
    if (file && file.type === 'text/csv') {
      setSelectedFiles(prev => ({ ...prev, [type]: file }));
      setUploadStatus(prev => ({ ...prev, [type]: '' }));
    } else {
      setUploadStatus(prev => ({ ...prev, [type]: 'error' }));
      alert('Please select a valid CSV file');
    }
  };

  const handleUpload = async (type) => {
    const file = selectedFiles[type];
    if (!file) {
      alert('Please select a file first');
      return;
    }

    setLoading(prev => ({ ...prev, [type]: true }));
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    try {
      const response = await axios.post('http://localhost:5000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data.success) {
        setUploadStatus(prev => ({ ...prev, [type]: 'success' }));
        setTimeout(() => {
          setSelectedFiles(prev => ({ ...prev, [type]: null }));
          setUploadStatus(prev => ({ ...prev, [type]: '' }));
        }, 3000);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus(prev => ({ ...prev, [type]: 'error' }));
    } finally {
      setLoading(prev => ({ ...prev, [type]: false }));
    }
  };

  const uploadSections = [
    {
      type: 'patients',
      title: 'Patients Data',
      description: 'Upload patient demographic information (CSV format)',
      color: '#3b82f6',
      example: 'PatientID, Name, Age, Gender, Contact'
    },
    {
      type: 'visits',
      title: 'Visits Data',
      description: 'Upload patient visit records (CSV format)',
      color: '#10b981',
      example: 'VisitID, PatientID, Date, Diagnosis, Doctor'
    },
    {
      type: 'prescriptions',
      title: 'Prescriptions Data',
      description: 'Upload prescription details (CSV format)',
      color: '#8b5cf6',
      example: 'PrescriptionID, VisitID, Medication, Dosage'
    }
  ];

  return (
    <div className="upload-container">
      <div className="page-header">
        <FaCloudUploadAlt className="page-icon" />
        <h1>Upload Healthcare Data</h1>
        <p>Upload CSV files to process and analyze healthcare data</p>
      </div>

      <div className="upload-grid">
        {uploadSections.map((section) => (
          <div key={section.type} className="upload-card" style={{'--border-color': section.color}}>
            <div className="upload-header" style={{borderLeftColor: section.color}}>
              <h2>{section.title}</h2>
              <p>{section.description}</p>
            </div>

            <div className="file-info">
              <small className="example-text">Expected format: {section.example}</small>
            </div>

            <div className="upload-body">
              <label htmlFor={`file-${section.type}`} className="file-input-label">
                <FaFileUpload />
                <span>
                  {selectedFiles[section.type] 
                    ? selectedFiles[section.type].name 
                    : 'Choose CSV file'}
                </span>
              </label>
              <input
                id={`file-${section.type}`}
                type="file"
                accept=".csv"
                onChange={(e) => handleFileSelect(e, section.type)}
                className="file-input"
              />

              <button
                onClick={() => handleUpload(section.type)}
                disabled={!selectedFiles[section.type] || loading[section.type]}
                className="btn btn-primary upload-btn"
                style={{background: section.color}}
              >
                {loading[section.type] ? (
                  <>
                    <div className="btn-spinner"></div>
                    Uploading...
                  </>
                ) : (
                  <>
                    <FaCloudUploadAlt />
                    Upload File
                  </>
                )}
              </button>
            </div>

            {uploadStatus[section.type] && (
              <div className={`upload-status ${uploadStatus[section.type]}`}>
                {uploadStatus[section.type] === 'success' ? (
                  <>
                    <FaCheckCircle />
                    File uploaded successfully!
                  </>
                ) : (
                  <>
                    <FaTimesCircle />
                    Upload failed. Please try again.
                  </>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="upload-info-section">
        <div className="info-card">
          <h3>Upload Guidelines</h3>
          <ul>
            <li>Files must be in CSV format</li>
            <li>Ensure column headers match the expected format</li>
            <li>Remove any special characters from data</li>
            <li>Maximum file size: 10MB</li>
            <li>Data will be validated before processing</li>
          </ul>
        </div>

        <div className="info-card">
          <h3>What Happens Next?</h3>
          <ul>
            <li>Files are uploaded to AWS S3 (raw data lake)</li>
            <li>Backend validates the data structure</li>
            <li>PySpark processes and cleans the data</li>
            <li>Cleaned data is stored for analytics</li>
            <li>View results in the Dashboard</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Upload;

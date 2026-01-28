import React, { useState } from 'react';
import { FaEdit, FaUser, FaStethoscope, FaPills, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import axios from 'axios';
import './DataEntry.css';

const DataEntry = () => {
  const [activeTab, setActiveTab] = useState('patient');
  const [submitStatus, setSubmitStatus] = useState({ type: '', message: '' });
  const [loading, setLoading] = useState(false);

  // Patient Form State
  const [patientData, setPatientData] = useState({
    patient_id: '',
    age: '',
    gender: '',
    location: '',
    bmi: '',
    smoker_status: '',
    alcohol_use: '',
    physical_activity_level: '',
    chronic_conditions: '',
    registration_date: '',
    insurance_type: ''
  });

  // Visit Form State
  const [visitData, setVisitData] = useState({
    visit_id: '',
    patient_id: '',
    visit_date: '',
    diagnosis_code: '',
    diagnosis_description: '',
    severity_score: '',
    blood_pressure: '',
    glucose_level: '',
    heart_rate: '',
    length_of_stay: '',
    previous_visit_gap_days: '',
    readmitted_within_30_days: ''
  });

  // Prescription Form State
  const [prescriptionData, setPrescriptionData] = useState({
    prescription_id: '',
    visit_id: '',
    patient_id: '',
    drug_name: '',
    drug_category: '',
    dosage: '',
    quantity: '',
    days_supply: '',
    prescribed_date: '',
    refill_count: ''
  });

  const handlePatientChange = (e) => {
    setPatientData({ ...patientData, [e.target.name]: e.target.value });
  };

  const handleVisitChange = (e) => {
    setVisitData({ ...visitData, [e.target.name]: e.target.value });
  };

  const handlePrescriptionChange = (e) => {
    setPrescriptionData({ ...prescriptionData, [e.target.name]: e.target.value });
  };

  const handlePatientSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/patient', patientData);
      console.log('Patient Response:', response);
      if (response.data.success || response.status === 201) {
        setSubmitStatus({ type: 'success', message: 'Patient registered successfully!' });
        setPatientData({ 
          patient_id: '', age: '', gender: '', location: '', bmi: '', 
          smoker_status: '', alcohol_use: '', physical_activity_level: '', 
          chronic_conditions: '', registration_date: '', insurance_type: '' 
        });
      } else {
        setSubmitStatus({ type: 'error', message: 'Failed to register patient. Please try again.' });
      }
    } catch (error) {
      console.error('Patient Error:', error);
      setSubmitStatus({ type: 'error', message: 'Failed to register patient. Please try again.' });
    } finally {
      setLoading(false);
      setTimeout(() => setSubmitStatus({ type: '', message: '' }), 5000);
    }
  };

  const handleVisitSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/visit', visitData);
      if (response.data.success) {
        setSubmitStatus({ type: 'success', message: 'Visit record added successfully!' });
        setVisitData({ 
          visit_id: '', patient_id: '', visit_date: '', diagnosis_code: '', 
          diagnosis_description: '', severity_score: '', blood_pressure: '', 
          glucose_level: '', heart_rate: '', length_of_stay: '', 
          previous_visit_gap_days: '', readmitted_within_30_days: '' 
        });
      }
    } catch (error) {
      setSubmitStatus({ type: 'error', message: 'Failed to add visit record. Please try again.' });
    } finally {
      setLoading(false);
      setTimeout(() => setSubmitStatus({ type: '', message: '' }), 5000);
    }
  };

  const handlePrescriptionSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/prescription', prescriptionData);
      if (response.data.success) {
        setSubmitStatus({ type: 'success', message: 'Prescription added successfully!' });
        setPrescriptionData({ 
          prescription_id: '', visit_id: '', patient_id: '', drug_name: '', 
          drug_category: '', dosage: '', quantity: '', days_supply: '', 
          prescribed_date: '', refill_count: '' 
        });
      }
    } catch (error) {
      setSubmitStatus({ type: 'error', message: 'Failed to add prescription. Please try again.' });
    } finally {
      setLoading(false);
      setTimeout(() => setSubmitStatus({ type: '', message: '' }), 5000);
    }
  };

  return (
    <div className="data-entry-container">
      <div className="page-header">
        <FaEdit className="page-icon" />
        <h1>Data Entry Forms</h1>
        <p>Enter real-time healthcare data directly into the system</p>
      </div>

      {submitStatus.message && (
        <div className={`alert alert-${submitStatus.type}`}>
          {submitStatus.type === 'success' ? <FaCheckCircle /> : <FaExclamationTriangle />}
          {submitStatus.message}
        </div>
      )}

      <div className="tabs-container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'patient' ? 'active' : ''}`}
            onClick={() => setActiveTab('patient')}
          >
            <FaUser />
            Patient Registration
          </button>
          <button
            className={`tab ${activeTab === 'visit' ? 'active' : ''}`}
            onClick={() => setActiveTab('visit')}
          >
            <FaStethoscope />
            Visit Details
          </button>
          <button
            className={`tab ${activeTab === 'prescription' ? 'active' : ''}`}
            onClick={() => setActiveTab('prescription')}
          >
            <FaPills />
            Prescription
          </button>
        </div>
      </div>

      <div className="form-container">
        {activeTab === 'patient' && (
          <form onSubmit={handlePatientSubmit} className="entry-form">
            <h2><FaUser /> Patient Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Patient ID *</label>
                <input
                  type="text"
                  name="patient_id"
                  value={patientData.patient_id}
                  onChange={handlePatientChange}
                  className="form-input"
                  required
                  placeholder="Enter patient ID"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Age *</label>
                <input
                  type="number"
                  name="age"
                  value={patientData.age}
                  onChange={handlePatientChange}
                  className="form-input"
                  required
                  min="0"
                  max="150"
                  placeholder="Enter age"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Gender *</label>
                <select
                  name="gender"
                  value={patientData.gender}
                  onChange={handlePatientChange}
                  className="form-select"
                  required
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Location *</label>
                <input
                  type="text"
                  name="location"
                  value={patientData.location}
                  onChange={handlePatientChange}
                  className="form-input"
                  required
                  placeholder="Enter location"
                />
              </div>

              <div className="form-group">
                <label className="form-label">BMI</label>
                <input
                  type="number"
                  step="0.1"
                  name="bmi"
                  value={patientData.bmi}
                  onChange={handlePatientChange}
                  className="form-input"
                  placeholder="Enter BMI"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Smoker Status</label>
                <select
                  name="smoker_status"
                  value={patientData.smoker_status}
                  onChange={handlePatientChange}
                  className="form-select"
                >
                  <option value="">Select Status</option>
                  <option value="Never">Never</option>
                  <option value="Former">Former</option>
                  <option value="Current">Current</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Alcohol Use</label>
                <select
                  name="alcohol_use"
                  value={patientData.alcohol_use}
                  onChange={handlePatientChange}
                  className="form-select"
                >
                  <option value="">Select Status</option>
                  <option value="None">None</option>
                  <option value="Moderate">Moderate</option>
                  <option value="Heavy">Heavy</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Physical Activity Level</label>
                <select
                  name="physical_activity_level"
                  value={patientData.physical_activity_level}
                  onChange={handlePatientChange}
                  className="form-select"
                >
                  <option value="">Select Level</option>
                  <option value="Sedentary">Sedentary</option>
                  <option value="Low">Low</option>
                  <option value="Moderate">Moderate</option>
                  <option value="High">High</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Insurance Type</label>
                <select
                  name="insurance_type"
                  value={patientData.insurance_type}
                  onChange={handlePatientChange}
                  className="form-select"
                >
                  <option value="">Select Insurance</option>
                  <option value="Private">Private</option>
                  <option value="Government">Government</option>
                  <option value="None">None</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Registration Date *</label>
                <input
                  type="date"
                  name="registration_date"
                  value={patientData.registration_date}
                  onChange={handlePatientChange}
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group full-width">
                <label className="form-label">Chronic Conditions</label>
                <textarea
                  name="chronic_conditions"
                  value={patientData.chronic_conditions}
                  onChange={handlePatientChange}
                  className="form-input"
                  rows="3"
                  placeholder="Enter chronic conditions (comma separated)"
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <div className="spinner"></div> : <><FaCheckCircle /> Register Patient</>}
            </button>
          </form>
        )}

        {activeTab === 'visit' && (
          <form onSubmit={handleVisitSubmit} className="entry-form">
            <h2><FaStethoscope /> Visit Information</h2>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Visit ID *</label>
                <input
                  type="text"
                  name="visit_id"
                  value={visitData.visit_id}
                  onChange={handleVisitChange}
                  className="form-input"
                  required
                  placeholder="Enter visit ID"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Patient ID *</label>
                <input
                  type="text"
                  name="patient_id"
                  value={visitData.patient_id}
                  onChange={handleVisitChange}
                  className="form-input"
                  required
                  placeholder="Enter patient ID"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Visit Date *</label>
                <input
                  type="date"
                  name="visit_date"
                  value={visitData.visit_date}
                  onChange={handleVisitChange}
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Diagnosis Code *</label>
                <input
                  type="text"
                  name="diagnosis_code"
                  value={visitData.diagnosis_code}
                  onChange={handleVisitChange}
                  className="form-input"
                  required
                  placeholder="Enter diagnosis code"
                />
              </div>

              <div className="form-group full-width">
                <label className="form-label">Diagnosis Description *</label>
                <input
                  type="text"
                  name="diagnosis_description"
                  value={visitData.diagnosis_description}
                  onChange={handleVisitChange}
                  className="form-input"
                  required
                  placeholder="Enter diagnosis description"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Severity Score</label>
                <input
                  type="number"
                  name="severity_score"
                  value={visitData.severity_score}
                  onChange={handleVisitChange}
                  className="form-input"
                  min="0"
                  max="10"
                  placeholder="0-10"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Blood Pressure</label>
                <input
                  type="text"
                  name="blood_pressure"
                  value={visitData.blood_pressure}
                  onChange={handleVisitChange}
                  className="form-input"
                  placeholder="e.g., 120/80"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Glucose Level</label>
                <input
                  type="number"
                  name="glucose_level"
                  value={visitData.glucose_level}
                  onChange={handleVisitChange}
                  className="form-input"
                  placeholder="mg/dL"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Heart Rate</label>
                <input
                  type="number"
                  name="heart_rate"
                  value={visitData.heart_rate}
                  onChange={handleVisitChange}
                  className="form-input"
                  placeholder="bpm"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Length of Stay (days)</label>
                <input
                  type="number"
                  name="length_of_stay"
                  value={visitData.length_of_stay}
                  onChange={handleVisitChange}
                  className="form-input"
                  placeholder="Number of days"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Previous Visit Gap (days)</label>
                <input
                  type="number"
                  name="previous_visit_gap_days"
                  value={visitData.previous_visit_gap_days}
                  onChange={handleVisitChange}
                  className="form-input"
                  placeholder="Days since last visit"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Readmitted Within 30 Days</label>
                <select
                  name="readmitted_within_30_days"
                  value={visitData.readmitted_within_30_days}
                  onChange={handleVisitChange}
                  className="form-select"
                >
                  <option value="">Select</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <div className="spinner"></div> : <><FaCheckCircle /> Add Visit Record</>}
            </button>
          </form>
        )}

        {activeTab === 'prescription' && (
          <form onSubmit={handlePrescriptionSubmit} className="entry-form">
            <h2><FaPills /> Prescription Details</h2>
            <div className="form-grid">
              <div className="form-group">
                <label className="form-label">Prescription ID *</label>
                <input
                  type="text"
                  name="prescription_id"
                  value={prescriptionData.prescription_id}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  required
                  placeholder="Enter prescription ID"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Visit ID *</label>
                <input
                  type="text"
                  name="visit_id"
                  value={prescriptionData.visit_id}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  required
                  placeholder="Enter visit ID"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Patient ID *</label>
                <input
                  type="text"
                  name="patient_id"
                  value={prescriptionData.patient_id}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  required
                  placeholder="Enter patient ID"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Drug Name *</label>
                <input
                  type="text"
                  name="drug_name"
                  value={prescriptionData.drug_name}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  required
                  placeholder="Enter drug name"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Drug Category</label>
                <select
                  name="drug_category"
                  value={prescriptionData.drug_category}
                  onChange={handlePrescriptionChange}
                  className="form-select"
                >
                  <option value="">Select Category</option>
                  <option value="Antibiotic">Antibiotic</option>
                  <option value="Analgesic">Analgesic</option>
                  <option value="Antihypertensive">Antihypertensive</option>
                  <option value="Antidiabetic">Antidiabetic</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Dosage *</label>
                <input
                  type="text"
                  name="dosage"
                  value={prescriptionData.dosage}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  required
                  placeholder="e.g., 500mg"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Quantity</label>
                <input
                  type="number"
                  name="quantity"
                  value={prescriptionData.quantity}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  placeholder="Number of units"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Days Supply</label>
                <input
                  type="number"
                  name="days_supply"
                  value={prescriptionData.days_supply}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  placeholder="Number of days"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Prescribed Date *</label>
                <input
                  type="date"
                  name="prescribed_date"
                  value={prescriptionData.prescribed_date}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Refill Count</label>
                <input
                  type="number"
                  name="refill_count"
                  value={prescriptionData.refill_count}
                  onChange={handlePrescriptionChange}
                  className="form-input"
                  min="0"
                  placeholder="Number of refills"
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <div className="spinner"></div> : <><FaCheckCircle /> Add Prescription</>}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default DataEntry;

CREATE DATABASE PHCSystemDB;
GO

USE PHCSystemDB;
GO

CREATE TABLE Locations (
    LocationID INT PRIMARY KEY IDENTITY(1,1),
    LocationName NVARCHAR(100) NOT NULL
);

INSERT INTO Locations (LocationName) VALUES 
('Avanigadda'), ('Repalle'), ('Pamarru'), ('Gudlavalleru');

CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY IDENTITY(1,1),
    DoctorName NVARCHAR(100) NOT NULL,
    Department_EN NVARCHAR(100) NOT NULL,
    Department_TE NVARCHAR(100) NOT NULL,
    LocationID INT FOREIGN KEY REFERENCES Locations(LocationID),
    RoomNo NVARCHAR(50) NOT NULL,
    IsAvailable BIT DEFAULT 1
);

INSERT INTO Doctors (DoctorName, Department_EN, Department_TE, LocationID, RoomNo, IsAvailable) VALUES
('Dr. K. Srinivas Rao', 'General Medicine', 'సాధారణ వైద్యము', 1, 'Room 101', 1),
('Dr. P. Lakshmi Devi', 'Pediatrics & Child Care', 'పిల్లల వైద్యము', 1, 'Room 104', 1),
('Dr. M. Ramanjaneyulu', 'Orthopedics', 'ఎముకల వైద్యము', 2, 'Room 102', 1),
('Dr. S. Swarna Latha', 'Gynecology & Obstetrics', 'స్త్రీ వైద్య నిపుణులు', 2, 'Room 105', 1),
('Dr. B. Ramesh Kumar', 'Ophthalmology (Eye Care)', 'కంటి వైద్య నిపుణులు', 3, 'Room 101', 1),
('Dr. V. Suresh Verma', 'General Medicine', 'సాధారణ వైద్యము', 3, 'Room 103', 1),
('Dr. Ch. Anitha', 'Dermatology (Skin Care)', 'చర్మ వైద్య నిపుణులు', 4, 'Room 101', 1),
('Dr. T. Venkat Ram', 'ENT Specialist', 'చెవి, ముక్కు, గొంతు వైద్యము', 4, 'Room 102', 1);

CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY IDENTITY(1,1),
    PatientUID NVARCHAR(50) NOT NULL,
    PatientName NVARCHAR(100) NOT NULL,
    DoctorID INT FOREIGN KEY REFERENCES Doctors(DoctorID),
    LocationID INT FOREIGN KEY REFERENCES Locations(LocationID),
    Slot NVARCHAR(50) NOT NULL,
    TokenNumber INT NOT NULL,
    BookingStatus NVARCHAR(50) DEFAULT 'Confirmed',
    CreatedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE PatientReports (
    ReportID INT PRIMARY KEY IDENTITY(1,1),
    PatientUID NVARCHAR(50) NOT NULL,
    DoctorName NVARCHAR(100) NOT NULL,
    ReportTitle NVARCHAR(150) NOT NULL,
    ReportDate DATE DEFAULT GETDATE(),
    DiagnosisSummary NVARCHAR(MAX),
    Status NVARCHAR(50) DEFAULT 'Completed'
);

INSERT INTO PatientReports (PatientUID, DoctorName, ReportTitle, ReportDate, DiagnosisSummary, Status) VALUES
('PAT-90812', 'Dr. K. Srinivas Rao', 'Complete Blood Count (CBC)', '2026-11-01', 'Hemoglobin levels normal (14.2 g/dL). No signs of anemia.', 'Completed');
# Database Design – Secure Healthcare Cloud Platform

## Objective

This document defines the initial PostgreSQL database design for the Secure Healthcare Cloud Platform.

## Initial Tables

### patients
Stores basic patient profile information.

### doctors
Stores doctor information including name, email, and specialization.

### appointments
Stores appointment bookings between patients and doctors.

## Relationships

- One patient can have many appointments.
- One doctor can have many appointments.
- Each appointment belongs to one patient and one doctor.

## Security Considerations

- No real patient data is used.
- Only test data is stored.
- Medical records are excluded from the initial schema.
- Future versions will include authentication, role-based access control, and audit logging.

## Next Steps

- Connect FastAPI to PostgreSQL.
- Create database models.
- Build patient API endpoints.

## Database Connectivity

The application uses SQLAlchemy to connect to PostgreSQL.

Configuration is loaded from environment variables using python-dotenv.

The `/db-health` endpoint validates connectivity by executing `SELECT 1`.


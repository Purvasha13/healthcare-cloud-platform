# 🏥 Secure Healthcare Cloud Platform

> **Independent Industry Project**
>
> A production-style Cloud Support & DevSecOps project demonstrating secure application deployment, cloud infrastructure, monitoring, security operations, and incident response using modern DevSecOps practices and cybersecurity tools.

---

# 📌 Project Overview

The **Secure Healthcare Cloud Platform** is an independent industry project created to simulate the responsibilities of a Graduate Cloud Support & DevSecOps Engineer working in a healthcare organisation.

The project combines software development, cloud engineering, DevSecOps, monitoring, cybersecurity, and operational support into a single production-style environment.

Rather than only building an application, this project focuses on how cloud engineers deploy, secure, monitor, troubleshoot, and continuously improve systems in real-world environments.

---

# 🎯 Project Objectives

This project aims to:

- Build a secure healthcare backend application
- Deploy applications using container technologies
- Learn Infrastructure as Code
- Implement CI/CD automation
- Perform security scanning throughout the development lifecycle
- Monitor application health and infrastructure
- Simulate production support incidents
- Investigate security events
- Produce operational documentation
- Follow DevSecOps best practices

---

# 🏥 Business Scenario

A fictional Melbourne healthcare organisation requires a secure cloud platform to manage:

- Patient information
- Doctor information
- Appointment scheduling
- Medical records
- Authentication
- Operational monitoring
- Security compliance

As the Cloud Support & DevSecOps Engineer, I am responsible for designing, deploying, securing, monitoring, maintaining, and supporting the platform.

---

# 🏗 Project Architecture

```text
                           Users
                              │
                       Postman / Browser
                              │
                              ▼
                     FastAPI Healthcare API
                              │
                    JWT Authentication
                              │
                              ▼
                      PostgreSQL Database
                              │
                              ▼
                     Docker Containers
                              │
                              ▼
                Kubernetes (Minikube Cluster)
                              │
      ┌───────────────────────┼──────────────────────┐
      │                       │                      │
      ▼                       ▼                      ▼
 GitHub Actions          Prometheus             Security Tools
     CI/CD                 Monitoring     (Trivy, CodeQL, Grype,
                                                Gitleaks)
      │                       │
      ▼                       ▼
 Incident Reports      Grafana Dashboard
      │
      ▼
 Operational Runbooks

# PCI-DSS Network Auditing & Risk Assessment Tool

An automated Python-based network auditing script developed for e-commerce security environments to assist with risk assessments and maintain compliance with **Payment Card Industry Data Security Standards (PCI-DSS)**.

---

## 🎯 Scenario & Objective
As a Junior Security Analyst protecting high-volume online transactions, this tool was built to proactively identify vulnerabilities within the company's network infrastructure. It helps detect misconfigured interfaces, unresponsive connections, and exposed services running on unauthorized open ports.

---

## ✨ Key Features
* **Interface Enumeration:** Lists all active IPv4 and IPv6 network interfaces.
* **Connectivity Verification:** Tests live network connectivity against reliable external IP addresses.
* **DNS Validation:** Resolves and communicates with known domains to verify DNS functionality.
* **Port & Process Auditing:** Scans open ports and inspects active processes to spot exposed or risky services.
* **Permission Guardrails:** Checks and handles administrative/root permissions safely before execution.

---

## 🛠️ Tech Stack & Environment
* **Language:** Python 3.12
* **Containerization:** Docker (Ubuntu 22.04 base image)
* **Development Environment:** VS Code

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Docker** installed on your local machine.

### 2. Pull & Run the Docker Container
The testing environment is packaged inside a custom Docker image. Spin up the container using:

```bash
docker run -it nwendlo1/c1w2m6 /bin/bash

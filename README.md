# Group 7 : Priority-Aware Network Management System for Emergency Bandwidth Allocation
This research project proposes a priority-aware network management system. 

## Project description
The system is designed to simulate and manage bandwidth allocation in a restrained network environment. The main objective of the system is to classify and prioritize traffic based on circumstantial parameters such as source identity (e.g., ambulance, police, hospital), request type (emergency vs. normal), and bandwidth availability. The reason for doing this is to provide emergency or time-sensitive communications assurance to always grant primary access to the network, while the rest could be made to be delayed or denied during peak usage.

**Tech Stack:**                              Python, Flask and SQLite from SQL-Alchemy

**Traffic Classification:**                  Rules-based tiering based on priority (Emergency, Critical, Normal, Best Effort)

**Web Dashboard and Virtual Simulator:**     Real-time visualization of traffic and performance

**Dynamic Bandwidth Manager:**               Adjusts resources in real time (Using Background Thread and free bandwidth function)

## System Block Diagram of Priority-Aware Bandwidth Allocation 
<img width="1536" height="1024" alt="System Block Diagram" src="https://github.com/user-attachments/assets/012386b2-6494-4f63-b2c8-ae0007aaa71f" />

## Methodology (Flow Chart)
<img width="400" height="800" alt="Methadology_flowchart" src="https://github.com/user-attachments/assets/16e5d778-ebc2-45d1-8576-942eacabd491"/>


**Implementation Stage 1:**
- Setup Backend Structure powered by SQLite + SQLAlchemy for real-time, accurate performance in vscode and install all dependencies.
- Design database architecture Model for real-time data logs.
- Setup Github repositories and authorization.
- Create a System Block Diagram.
- Create a Methodology (Flow Chart)
- Build source for Webpage data design (Index.html)
- Build source for Simulator (logic.py)

**Implementation Stage 2:**
- Design Database Structure and webpage design for Dashboard and Simulator
- Design Backend side for Priority- based queue handling for scalability
- Handle backend side for background Threads for system logs
- Design Handlers for Removal of expired logs post duration to free space & ensure accuracy
- Define backend handlers for Datalogs Display dashboard.
- Create Timestamps and Verified sources for Validation.
- Create auto cleanup scripts to refresh outdated contexts.
- Code refinement and errors resolves for overall application.


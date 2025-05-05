it_jobs = [
    # Software Development & Engineering
    "Senior Frontend Developer",
    "Backend Developer",
    "Full-Stack Developer",
    "Mobile App Developer (iOS/Android)",
    "Game Developer",
    "Embedded Systems Engineer",
    "DevOps Engineer",
    "Software Architect",
    "QA Engineer (Manual Testing)",
    "Automation Test Engineer",
    "Firmware Engineer",
    "UI/UX Developer",
    "Technical Lead",
    "Scrum Master",
    "Agile Coach",
    
    # Data & AI/ML
    "Data Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Research Scientist",
    "Data Analyst",
    "Business Intelligence (BI) Analyst",
    "Data Architect",
    "Big Data Engineer",
    "ETL Developer",
    "NLP Engineer",
    "Computer Vision Engineer",
    "MLOps Engineer",
    
    # Cloud & SysOps
    "Cloud Engineer (AWS/Azure/GCP)",
    "Cloud Architect",
    "Site Reliability Engineer (SRE)",
    "Systems Administrator",
    "Network Engineer",
    "Database Administrator (DBA)",
    "Linux Administrator",
    "Virtualization Engineer",
    "Kubernetes Engineer",
    
    # Cybersecurity
    "Cybersecurity Analyst",
    "Ethical Hacker/Penetration Tester",
    "Security Engineer",
    "Security Architect",
    "Incident Responder",
    "Forensic Analyst",
    "GRC (Governance, Risk, Compliance) Specialist",
    "Security Consultant",
    "Threat Intelligence Analyst",
    
    # IT Support & Management
    "IT Support Specialist",
    "Helpdesk Technician",
    "IT Project Manager",
    "IT Director",
    "Chief Technology Officer (CTO)",
    "IT Consultant",
    "Technical Writer",
    "Solutions Architect",
    
    # Emerging Tech & Niche Roles
    "Blockchain Developer",
    "AR/VR Developer",
    "Quantum Computing Engineer",
    "IoT Engineer",
    "Robotics Engineer",
    "5G Network Engineer",
    "Edge Computing Engineer",
    
    # Sales & Customer-Facing Tech Roles
    "Sales Engineer",
    "Pre-Sales Consultant",
    "Technical Account Manager",
    "Customer Success Engineer",
    "Product Manager (Technical)",
    "Product Owner"
]
from pyspark.sql.types import *

dataframe_schema= StructType([
    StructField("category", StringType(), True),
    StructField("company", StringType(), True),
    StructField("description", StringType(), True),
    StructField("id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("location_hierarchy", ArrayType(StringType(), True), True),
    StructField("posted_date", StringType(), True),
    StructField("salary_is_predicted", LongType(), True),
    StructField("salary_max", DoubleType(), True),
    StructField("salary_min", DoubleType(), True),
    StructField("title", StringType(), True),
    StructField("url", StringType(), True)
])
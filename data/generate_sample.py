"""Run once to generate sample_resumes.csv from Kaggle dataset or synthetic data."""
import pandas as pd
import os

SAMPLE_RESUMES = [
    {
        "Category": "Data Science",
        "Resume": """John Smith\njohn.smith@email.com | +1-555-0101 | linkedin.com/in/johnsmith

SUMMARY
Data Scientist with 5 years of experience in machine learning and statistical analysis.

SKILLS
Python, Machine Learning, TensorFlow, scikit-learn, Pandas, SQL, Statistics, NLP, Deep Learning, Jupyter

EXPERIENCE
Senior Data Scientist | TechCorp Inc | Jan 2021 – Present
- Built predictive models using Python and scikit-learn
- Led team of 3 data scientists

Data Scientist | Analytics Co | Jun 2019 – Dec 2020
- Developed NLP pipeline for text classification

EDUCATION
M.S. Data Science
Stanford University | 2019
B.S. Computer Science
MIT | 2017
"""
    },
    {
        "Category": "Web Developer",
        "Resume": """Jane Doe\njane.doe@gmail.com | +44-7700-900123 | linkedin.com/in/janedoe

PROFILE
Full-stack developer specializing in React and Node.js applications.

TECHNICAL SKILLS
JavaScript, React, Node.js, TypeScript, REST API, MongoDB, Docker, Git, AWS, Agile

WORK HISTORY
Frontend Lead | StartupXYZ | Mar 2022 – Present
- Built React dashboard serving 50k users

Full Stack Developer | WebAgency | Aug 2020 – Feb 2022
- Developed REST APIs with Node.js and Express

EDUCATION
B.Sc Computer Science
University of Manchester | 2020
"""
    },
    {
        "Category": "DevOps Engineer",
        "Resume": """Carlos Rivera\ncarlos.r@protonmail.com | +1-800-555-0199

ABOUT ME
DevOps engineer with expertise in cloud infrastructure and CI/CD pipelines.

SKILLS
AWS, Docker, Kubernetes, Terraform, Jenkins, CI/CD, Linux, Bash, Python, Git, Ansible

EXPERIENCE
DevOps Engineer | CloudSystems Ltd | Feb 2020 – Present
- Managed Kubernetes clusters on AWS EKS

Junior DevOps | FinTech Solutions | Jan 2018 – Jan 2020
- Built CI/CD pipelines with Jenkins and GitHub Actions

EDUCATION
B.E. Information Technology
IIT Bombay | 2017
"""
    },
    {
        "Category": "Business Analyst",
        "Resume": """Priya Sharma\npriya.sharma@outlook.com | +91-9876543210 | linkedin.com/in/priyasharma

OBJECTIVE
Business Analyst with strong analytical skills and experience in data-driven decision making.

KEY SKILLS
Excel, SQL, Power BI, Tableau, Data Analysis, Project Management, Agile, Communication, Leadership, Statistics

EXPERIENCE
Senior Business Analyst | MegaCorp | Apr 2021 – Present
- Created Power BI dashboards for C-suite reporting

Business Analyst | Consulting Group | Jul 2018 – Mar 2021
- Conducted requirements gathering and process mapping

EDUCATION
MBA (Finance & Analytics)
Indian School of Business | 2018
B.Com
Delhi University | 2016
"""
    },
    {
        "Category": "Machine Learning Engineer",
        "Resume": """Alex Johnson\nalex.j@techmail.io | +1-415-555-0177 | linkedin.com/in/alexjohnson-ml

SUMMARY
ML Engineer with focus on NLP and computer vision systems at scale.

TECHNICAL EXPERTISE
Python, PyTorch, TensorFlow, Deep Learning, NLP, Hugging Face, Transformers, OpenCV,
Spark, Hadoop, AWS, Docker, Kubernetes, FastAPI, Git, CI/CD, MLflow

EXPERIENCE
ML Engineer | AI Labs Inc | Sep 2020 – Present
- Trained transformer models for document classification

Research Engineer | University AI Lab | Aug 2019 – Aug 2020
- Published 2 papers on sequence modeling

EDUCATION
M.S. Artificial Intelligence
Carnegie Mellon University | 2019
B.S. Mathematics
UC Berkeley | 2017
"""
    },
    {
        "Category": "Software Engineer",
        "Resume": """Fatima Al-Hassan\nfatima.hassan@email.com | +971-50-123-4567

PROFILE
Software Engineer with expertise in backend systems and distributed architectures.

SKILLS
Java, Python, Microservices, PostgreSQL, Redis, Kafka, Docker, Kubernetes, REST API, Git, Scrum

EXPERIENCE
Backend Engineer | FinPlatform | Jan 2022 – Present
- Built microservices handling 1M+ transactions/day using Java and Kafka

Software Engineer | E-commerce Giant | Jun 2019 – Dec 2021
- Developed order management system with PostgreSQL

EDUCATION
B.Sc Software Engineering
American University of Dubai | 2019
"""
    },
    {
        "Category": "Data Engineer",
        "Resume": """Liang Wei\nliang.wei@datamail.com | +86-138-0000-1234 | linkedin.com/in/liangwei

SUMMARY
Data Engineer specialized in building scalable ETL pipelines and data warehouses.

CORE SKILLS
Python, SQL, Spark, Hadoop, Airflow, dbt, Snowflake, BigQuery, Redshift, Kafka, AWS, Docker, Git

EXPERIENCE
Senior Data Engineer | DataCorp | Mar 2021 – Present
- Designed Snowflake data warehouse for marketing analytics

Data Engineer | TechStartup | Jan 2019 – Feb 2021
- Built Airflow DAGs processing 10TB+ daily

EDUCATION
M.S. Computer Science
Tsinghua University | 2018
B.S. Information Systems
Peking University | 2016
"""
    },
    {
        "Category": "UX Designer",
        "Resume": """Maria Santos\nmaria.santos@design.com | +55-11-98765-4321 | linkedin.com/in/mariasantos

ABOUT
Creative UX Designer with 4 years creating intuitive digital experiences.

SKILLS
Figma, Adobe Photoshop, UX Research, Communication, Project Management, Agile, JavaScript, React

EXPERIENCE
Senior UX Designer | DesignStudio | Feb 2022 – Present
- Led UX redesign increasing user retention by 30%

UX Designer | AppCompany | Aug 2020 – Jan 2022
- Conducted user research and usability testing

EDUCATION
Bachelor of Design (Interaction Design)
ESDI Rio de Janeiro | 2020
"""
    },
]


def create_sample_csv():
    out_path = os.path.join(os.path.dirname(__file__), "sample_resumes.csv")
    df = pd.DataFrame(SAMPLE_RESUMES)
    df.to_csv(out_path, index=False)
    print(f"Created {out_path} with {len(df)} rows")


if __name__ == "__main__":
    create_sample_csv()

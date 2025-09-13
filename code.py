import streamlit as st
import json
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="Tech Career Roadmap Tracker",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state for progress tracking
if 'progress' not in st.session_state:
    st.session_state.progress = {}

if 'start_date' not in st.session_state:
    st.session_state.start_date = datetime.now().date()

if 'selected_track' not in st.session_state:
    st.session_state.selected_track = "CS Fresher"


# 1. ADD THIS TO SESSION STATE INITIALIZATION (after existing session state)
if 'notes' not in st.session_state:
    st.session_state.notes = {}

PROGRESS_FILE = "progress_data.json"

SOFTWARE_ENGINEER_ROADMAP = {

    "Phase 1: Programming Fundamentals": {
        "duration": "2-3 months",
        "topics": {
            "Computer Science Basics": [
                "How computers work: CPU, Memory, Storage",
                "Binary, hexadecimal number systems",
                "Operating system basics",
                "Command line/Terminal basics"
            ],
            "First Programming Language (Python/JavaScript)": [
                "Variables, data types, operators",
                "Control flow: if/else, loops",
                "Functions and scope",
                "Basic input/output operations",
                "Error handling basics"
            ],
            "Problem Solving": [
                "Breaking down problems",
                "Pseudocode writing",
                "Basic debugging techniques",
                "Reading documentation"
            ]
        },
        "resources": {
            "Free Courses": [
                "CS50x - Harvard's Introduction to Computer Science (edX - free)",
                "Python for Everybody - University of Michigan (Coursera - audit free)",
                "The Odin Project - Foundations (completely free)",
                "freeCodeCamp.org - Responsive Web Design & JavaScript (free)",
                "Codecademy - Learn Python 3 (free tier)"
            ],
            "YouTube Playlists": [
                "Python Tutorial for Beginners - Programming with Mosh",
                "CS50 2024 Lectures - Harvard University",
                "Learn JavaScript - Full Course for Beginners - freeCodeCamp.org",
                "Python Programming Tutorial - Derek Banas",
                "Computer Science Basics - Crash Course Computer Science"
            ],
            "Free Books & Websites": [
                "Automate the Boring Stuff with Python (free online)",
                "Eloquent JavaScript by Marijn Haverbeke (free online)",
                "Learn Python the Hard Way (free online version)",
                "Mozilla Developer Network (MDN) Web Docs",
                "W3Schools - Programming tutorials"
            ],
            "Interactive Practice (Free)": [
                "Codecademy (free tier)",
                "freeCodeCamp.org",
                "Khan Academy - Intro to Programming",
                "Scratch.mit.edu (visual programming)",
                "Python.org tutorial"
            ]
        }
    },

    "Phase 2: Core Computer Science Fundamentals": {
        "duration": "3-4 months",
        "topics": {
            "Operating Systems": [
                "Process management and scheduling",
                "Memory management: Virtual memory, paging, segmentation",
                "File systems: FAT, NTFS, ext4, journaling",
                "Concurrency: Threads, synchronization, deadlocks",
                "I/O systems and device drivers",
                "System calls and kernel modes",
                "Distributed operating systems basics"
            ],
            "Computer Networks": [
                "OSI and TCP/IP model",
                "Physical layer: Cables, wireless, signal transmission",
                "Data link layer: Ethernet, MAC addresses, switching",
                "Network layer: IP addressing, routing protocols (OSPF, BGP)",
                "Transport layer: TCP vs UDP, port numbers, congestion control",
                "Application layer: HTTP/HTTPS, DNS, DHCP, FTP, SMTP",
                "Network security: Firewalls, VPNs, encryption",
                "Network troubleshooting and tools (ping, traceroute, wireshark)"
            ],
            "Database Management Systems": [
                "Database models: Relational, hierarchical, network",
                "Relational algebra and calculus",
                "SQL fundamentals: DDL, DML, DCL, TCL",
                "Advanced SQL: Joins, subqueries, window functions, CTEs",
                "Database design: ER diagrams, normalization (1NF to BCNF)",
                "Transaction management: ACID properties",
                "Concurrency control: Locking, isolation levels",
                "Indexing: B-trees, Hash indexes, bitmap indexes",
                "Query optimization and execution plans",
                "Database recovery and backup strategies",
                "NoSQL databases: Document, Key-value, Column-family, Graph"
            ],
            "Computer Architecture": [
                "CPU architecture: RISC vs CISC, pipelining",
                "Memory hierarchy: Cache, RAM, storage",
                "Instruction set architecture (ISA)",
                "Assembly language basics",
                "Multicore and parallel processing",
                "GPU architecture and parallel computing"
            ],
            "Discrete Mathematics": [
                "Set theory and logic",
                "Graph theory fundamentals",
                "Combinatorics and probability",
                "Number theory basics",
                "Boolean algebra",
                "Mathematical induction and proof techniques"
            ]
        },
        "resources": {
            "Free University Courses": [
                "Operating Systems - UC Berkeley CS162 (YouTube)",
                "Computer Networks - Stanford CS144 (YouTube)",
                "Database Systems - CMU 15-445 (YouTube + materials)",
                "Computer Architecture - Princeton (Coursera - audit free)",
                "Discrete Mathematics - MIT 6.042J (MIT OpenCourseWare)",
                "NPTEL - Operating Systems (Indian Institute of Technology)"
            ],
            "YouTube Channels & Playlists": [
                "Operating Systems by Gate Smashers",
                "Computer Networks by Gate Smashers",
                "Database Management System by Knowledge Gate",
                "Computer Architecture by Neso Academy",
                "Discrete Mathematics by Trefor Bazett",
                "CS162 Operating Systems - UC Berkeley (official)"
            ],
            "Free Books & Resources": [
                "Operating System Concepts (9th edition) - selected chapters free online",
                "Computer Networking: A Top-Down Approach - companion website",
                "Database System Concepts - companion materials",
                "GeeksforGeeks - comprehensive CS topics",
                "Tutorialspoint - computer science fundamentals",
                "MIT OpenCourseWare - Mathematics for Computer Science"
            ],
            "Interactive Platforms": [
                "SQLBolt - Interactive SQL tutorial (free)",
                "W3Schools SQL Tutorial (free)",
                "HackerRank - Database track (free tier)",
                "MySQL Tutorial - MySQL.com (free)",
                "PostgreSQL Tutorial - PostgreSQLTutorial.com (free)",
                "Khan Academy - Computer Science courses"
            ]
        }
    },

    "Phase 3: Data Structures & Algorithms": {
        "duration": "3-4 months",
        "topics": {
            "Basic Data Structures": [
                "Arrays and dynamic arrays",
                "Linked Lists (singly, doubly)",
                "Stacks and Queues",
                "Hash Tables/Maps",
                "Sets"
            ],
            "Advanced Data Structures": [
                "Trees (Binary, BST, AVL, Red-Black)",
                "Heaps and Priority Queues",
                "Graphs (directed, undirected)",
                "Tries",
                "Union-Find (Disjoint Set)",
                "Segment Trees and Fenwick Trees",
                "Bloom Filters"
            ],
            "Algorithms": [
                "Sorting: Bubble, Selection, Insertion, Merge, Quick, Heap, Radix",
                "Searching: Linear, Binary, DFS, BFS",
                "Dynamic Programming: Memoization, tabulation",
                "Greedy Algorithms",
                "Backtracking",
                "Graph algorithms: Dijkstra's, Bellman-Ford, Floyd-Warshall, A*",
                "String algorithms: KMP, Rabin-Karp, suffix arrays",
                "Number theory algorithms: GCD, prime generation"
            ],
            "Complexity Analysis": [
                "Big O notation",
                "Time complexity analysis",
                "Space complexity analysis",
                "Best, average, worst case analysis",
                "Amortized analysis"
            ]
        },
        "resources": {
            "Free University Courses": [
                "Algorithms Part I & II - Princeton (Coursera - audit free)",
                "Data Structures and Algorithms - UC San Diego (Coursera - audit free)",
                "MIT 6.006 Introduction to Algorithms (MIT OpenCourseWare)",
                "Stanford CS161 Design and Analysis of Algorithms (YouTube)",
                "Harvard CS224 Advanced Algorithms (YouTube)"
            ],
            "YouTube Channels & Playlists": [
                "Data Structures and Algorithms by Abdul Bari",
                "Algorithms Explained by Back To Back SWE",
                "Data Structures Full Course by freeCodeCamp",
                "MIT 6.006 Introduction to Algorithms (official)",
                "Algorithms by William Fiset",
                "Data Structures and Algorithms by Neso Academy"
            ],
            "Free Books & Websites": [
                "Algorithms by Jeff Erickson (free PDF)",
                "Open Data Structures by Pat Morin (free online)",
                "GeeksforGeeks - Data Structures and Algorithms",
                "VisuAlgo - Algorithm Visualizations (free)",
                "Algorithm Visualizer (algorithm-visualizer.org)",
                "Big-O Cheat Sheet (bigocheatsheet.com)"
            ],
            "Coding Practice Platforms": [
                "LeetCode (free tier with 50+ problems)",
                "HackerRank Data Structures track (free)",
                "CodeChef - Practice problems (free)",
                "AtCoder - Competitive programming (free)",
                "Codeforces - Competitive programming (free)",
                "InterviewBit - Programming track (free tier)"
            ]
        }
    },

    "Phase 4: Web Development Fundamentals": {
        "duration": "3-4 months",
        "topics": {
            "Frontend Basics": [
                "HTML5: Semantic markup, forms, accessibility",
                "CSS3: Flexbox, Grid, animations, responsive design",
                "JavaScript: DOM manipulation, events, async programming",
                "Browser DevTools mastery",
                "Web Performance Optimization",
                "Cross-browser compatibility"
            ],
            "Backend Basics": [
                "HTTP/HTTPS protocols in depth",
                "RESTful API design and best practices",
                "Server-side programming (Node.js/Python/Java)",
                "Authentication & Authorization (JWT, OAuth 2.0, SAML)",
                "Session management and cookies",
                "WebSockets and real-time communication",
                "API documentation (OpenAPI/Swagger)"
            ],
            "Databases": [
                "Advanced SQL: Window functions, CTEs, stored procedures",
                "Relational databases: PostgreSQL, MySQL advanced features",
                "NoSQL databases: MongoDB, Redis, Cassandra, DynamoDB",
                "Database design and normalization",
                "ORMs and Query builders",
                "Database migrations and versioning",
                "Database performance tuning"
            ],
            "Version Control": [
                "Git fundamentals and advanced commands",
                "Branching strategies (Git Flow, GitHub Flow, GitLab Flow)",
                "Pull requests and code reviews",
                "Resolving merge conflicts",
                "Git hooks and automation",
                "Semantic versioning"
            ]
        },
        "resources": {
            "Free Comprehensive Courses": [
                "The Odin Project - Full Stack JavaScript (completely free)",
                "Full Stack Open - University of Helsinki (free)",
                "CS50's Web Programming with Python and JavaScript (edX - free)",
                "freeCodeCamp - Full Stack Development (free)",
                "Web Development Bootcamp by Colt Steele (YouTube version)"
            ],
            "YouTube Channels & Playlists": [
                "HTML Full Course by SuperSimpleDev",
                "CSS Complete Course by Dave Gray",
                "JavaScript Full Course by Programming with Mosh",
                "Node.js Tutorial by The Net Ninja",
                "Git and GitHub for Beginners by freeCodeCamp",
                "RESTful APIs Tutorial by Programming with Mosh"
            ],
            "Free Documentation & Tutorials": [
                "MDN Web Docs - HTML, CSS, JavaScript (mozilla.org)",
                "W3Schools - Web Development tutorials (free)",
                "JavaScript.info - The Modern JavaScript Tutorial (free)",
                "Node.js official documentation and guides",
                "Express.js official documentation",
                "Git Documentation (git-scm.com)"
            ],
            "Interactive Learning Platforms": [
                "freeCodeCamp - Responsive Web Design (free certification)",
                "Codecademy - Web Development paths (free tier)",
                "Frontend Mentor - Real-world projects (free tier)",
                "CSS Grid Garden - CSS Grid game (free)",
                "Flexbox Froggy - Flexbox game (free)",
                "Git Immersion - Interactive Git tutorial (free)"
            ],
            "Free Database Resources": [
                "PostgreSQL Tutorial (postgresqltutorial.com)",
                "MySQL Tutorial (mysqltutorial.org)",
                "MongoDB University (free courses)",
                "SQLBolt - Interactive SQL lessons",
                "W3Schools SQL Tutorial",
                "Database Design Course by freeCodeCamp (YouTube)"
            ]
        }
    },

    "Phase 5: Modern Frameworks & Tools": {
        "duration": "3-4 months",
        "topics": {
            "Frontend Frameworks": [
                "React.js: Components, hooks, state management",
                "Vue.js or Angular basics",
                "State management: Redux, Context API, Zustand",
                "Next.js/Nuxt.js for SSR/SSG",
                "CSS frameworks: Tailwind, Material-UI",
                "TypeScript for type safety"
            ],
            "Backend Frameworks": [
                "Express.js/Fastify (Node.js)",
                "Django/FastAPI (Python)",
                "Spring Boot (Java)",
                "GraphQL basics",
                "Microservices architecture",
                "Message queues: RabbitMQ, Apache Kafka"
            ],
            "Development Tools": [
                "Package managers: npm, yarn, pip",
                "Build tools: Webpack, Vite, Rollup",
                "Testing: Jest, Pytest, Cypress, Playwright",
                "CI/CD pipelines",
                "Docker containerization",
                "Code quality tools: ESLint, Prettier, SonarQube"
            ],
            "Cloud Platforms": [
                "AWS basics: EC2, S3, Lambda, RDS, VPC",
                "Google Cloud Platform or Azure",
                "Serverless architecture",
                "CDN and caching strategies",
                "Infrastructure as Code: Terraform, CloudFormation"
            ]
        },
        "resources": {
            "Free React Resources": [
                "React Official Tutorial and Documentation (reactjs.org)",
                "React Course by freeCodeCamp (YouTube - 10+ hours)",
                "Full Stack React & Next.js by The Net Ninja (YouTube)",
                "React Tutorial by Programming with Mosh (YouTube)",
                "Scrimba - Learn React for Free (interactive)",
                "Epic React by Kent C. Dodds (free articles and resources)"
            ],
            "Free Backend Framework Resources": [
                "Express.js Official Documentation and Guides",
                "Django Official Tutorial (docs.djangoproject.com)",
                "FastAPI Official Tutorial (fastapi.tiangolo.com)",
                "Node.js and Express Course by freeCodeCamp (YouTube)",
                "Django Tutorial by Corey Schafer (YouTube)",
                "Python Django Web Framework by MDN (free)"
            ],
            "Free TypeScript Resources": [
                "TypeScript Official Handbook (typescriptlang.org)",
                "TypeScript Course by freeCodeCamp (YouTube)",
                "TypeScript Deep Dive by Basarat Ali Syed (free online book)",
                "Learn TypeScript by The Net Ninja (YouTube)",
                "TypeScript Tutorial by Programming with Mosh (YouTube)"
            ],
            "Free Cloud & DevOps Resources": [
                "AWS Free Tier and Documentation",
                "Google Cloud Free Tier and Qwiklabs",
                "Azure Free Account and Microsoft Learn",
                "Docker Official Documentation and Play with Docker",
                "Docker Tutorial by TechWorld with Nana (YouTube)",
                "AWS Course by freeCodeCamp (YouTube - 10+ hours)"
            ],
            "Free Testing Resources": [
                "Jest Official Documentation",
                "Testing JavaScript Applications by Kent C. Dodds (free articles)",
                "Cypress Documentation and Real World App",
                "Testing Tutorial by The Net Ninja (YouTube)",
                "Unit Testing Course by freeCodeCamp (YouTube)",
                "Test Driven Development by Fun Fun Function (YouTube)"
            ]
        }
    },

    "Phase 6: Software Engineering Practices": {
        "duration": "2-3 months",
        "topics": {
            "Design Patterns": [
                "Creational: Singleton, Factory, Builder",
                "Structural: Adapter, Decorator, Facade",
                "Behavioral: Observer, Strategy, Command",
                "MVC, MVP, MVVM architectures",
                "SOLID principles",
                "Dependency Injection"
            ],
            "Testing": [
                "Unit testing",
                "Integration testing",
                "End-to-end testing",
                "Test-Driven Development (TDD)",
                "Behavior-Driven Development (BDD)",
                "Property-based testing",
                "Performance and load testing"
            ],
            "Code Quality": [
                "Clean code principles",
                "Code reviews best practices",
                "Refactoring techniques",
                "Documentation",
                "Linting and formatting",
                "Static code analysis",
                "Technical debt management"
            ],
            "Agile & Project Management": [
                "Scrum methodology",
                "Kanban boards",
                "Sprint planning and retrospectives",
                "User stories and estimation",
                "JIRA/Linear/Trello",
                "DevOps culture and practices"
            ]
        },
        "resources": {
            "Free Design Patterns Resources": [
                "Refactoring.Guru - Design Patterns (free online)",
                "Design Patterns by Christopher Okhravi (YouTube series)",
                "Java Design Patterns by Derek Banas (YouTube)",
                "Head First Design Patterns - selected chapters (free samples)",
                "SOLID Principles by Uncle Bob Martin (YouTube)",
                "Design Patterns in Plain English by Mosh Hamedani (YouTube)"
            ],
            "Free Testing Resources": [
                "Test Driven Development - Introduction by freeCodeCamp",
                "TDD Course by Fun Fun Function (YouTube)",
                "Unit Testing Best Practices by Microsoft Docs (free)",
                "Testing Pyramid by Martin Fowler (free articles)",
                "Cypress Real World App (free open source project)",
                "Jest Documentation and Examples (free)"
            ],
            "Free Clean Code Resources": [
                "Clean Code - Uncle Bob Martin lectures (YouTube)",
                "Clean Code Summary by FreeCodeCamp (free articles)",
                "Code Review Best Practices by Google (free documentation)",
                "Refactoring.com by Martin Fowler (free articles)",
                "Clean Architecture by Uncle Bob (YouTube talks)",
                "Code Quality Tools Documentation (ESLint, Prettier, SonarQube)"
            ],
            "Free Agile Resources": [
                "Scrum Guide (scrumguides.org - official and free)",
                "Agile Manifesto and Principles (agilemanifesto.org)",
                "Kanban Guide by Atlassian (free)",
                "Agile and Scrum Course by freeCodeCamp (YouTube)",
                "Project Management by Google Career Certificates (Coursera - audit free)",
                "DevOps Culture by Atlassian (free guides)"
            ]
        }
    },

    "Phase 7: System Design & Architecture": {
        "duration": "3-4 months",
        "topics": {
            "System Design Fundamentals": [
                "Scalability: Horizontal vs Vertical",
                "Load balancing strategies",
                "Caching: Browser, CDN, Application, Database",
                "Database sharding and replication",
                "CAP theorem and consistency models",
                "Partitioning and data distribution"
            ],
            "Distributed Systems": [
                "Microservices vs Monolithic",
                "Service discovery",
                "Message queues: RabbitMQ, Kafka, Amazon SQS",
                "API Gateway patterns",
                "Event-driven architecture",
                "Consensus algorithms: Raft, Paxos",
                "Distributed transactions and 2PC"
            ],
            "Performance & Optimization": [
                "Performance profiling",
                "Database query optimization",
                "Caching strategies",
                "Lazy loading and code splitting",
                "CDN optimization",
                "Network latency optimization"
            ],
            "Security": [
                "OWASP Top 10",
                "Authentication: JWT, OAuth 2.0, SAML",
                "Encryption and hashing",
                "SQL injection prevention",
                "XSS and CSRF protection",
                "Zero-trust architecture",
                "Security testing and auditing"
            ]
        },
        "resources": {
            "Free System Design Courses": [
                "MIT 6.824 Distributed Systems (YouTube + materials)",
                "System Design Primer (GitHub repository - free)",
                "High Scalability website (free articles)",
                "System Design Interview videos by Gaurav Sen (YouTube)",
                "Distributed Systems Course by Martin Kleppmann (YouTube)",
                "Grokking System Design - free articles and examples"
            ],
            "Free YouTube Resources": [
                "System Design Interview by Gaurav Sen",
                "System Design by Tech Dummies",
                "Distributed Systems by Martin Kleppmann",
                "Database Engineering by Hussein Nasser",
                "System Design Concepts by ByteByteGo",
                "Microservices by TechWorld with Nana"
            ],
            "Free Security Resources": [
                "OWASP Official Documentation (free)",
                "Web Application Security by OWASP (free)",
                "Cybersecurity Course by freeCodeCamp (YouTube)",
                "Authentication and Authorization by Auth0 (free resources)",
                "Security Engineering by Ross Anderson (free PDF)",
                "Web Security Academy by PortSwigger (free)"
            ],
            "Free Architecture Resources": [
                "AWS Architecture Center (free)",
                "Google Cloud Architecture Center (free)",
                "Martin Fowler's website (free articles)",
                "Microservices.io by Chris Richardson (free patterns)",
                "12 Factor App methodology (free)",
                "Clean Architecture by Uncle Bob (free articles and talks)"
            ]
        }
    },

    "Phase 8: Advanced Backend Development": {
        "duration": "3-4 months",
        "topics": {
            "Advanced Database Concepts": [
                "Transaction isolation levels",
                "Database indexing strategies",
                "Query optimization and execution plans",
                "Database migrations",
                "Time-series databases",
                "Graph databases: Neo4j, Amazon Neptune",
                "Database clustering and high availability"
            ],
            "API Development": [
                "RESTful API best practices",
                "GraphQL implementation and optimization",
                "gRPC and Protocol Buffers",
                "API versioning strategies",
                "Rate limiting and throttling",
                "API security and authentication",
                "API monitoring and analytics"
            ],
            "Real-time Systems": [
                "WebSockets implementation",
                "Server-Sent Events (SSE)",
                "Long polling",
                "Real-time databases (Firebase, Supabase)",
                "Push notifications",
                "Event sourcing and CQRS"
            ],
            "Search & Analytics": [
                "Elasticsearch implementation",
                "Full-text search optimization",
                "Analytics pipelines",
                "Log aggregation",
                "Monitoring and alerting",
                "Data warehousing concepts",
                "ETL/ELT processes"
            ]
        },
        "resources": {
            "Free Database Resources": [
                "PostgreSQL Documentation (comprehensive and free)",
                "MySQL Documentation and Tutorials (free)",
                "Database Internals Course by Hussein Nasser (YouTube)",
                "SQL Performance Explained by Markus Winand (free online)",
                "Database Design Course by freeCodeCamp (YouTube)",
                "Neo4j Graph Academy (free courses)"
            ],
            "Free API Development Resources": [
                "RESTful API Design by Microsoft (free documentation)",
                "GraphQL Official Documentation and Tutorial",
                "How to GraphQL - free tutorial",
                "API Design Guide by Google (free)",
                "OpenAPI Specification Documentation (free)",
                "Postman Learning Center (free)"
            ],
            "Free Real-time Systems Resources": [
                "WebSocket Tutorial by Mozilla MDN (free)",
                "Real-time Web Technologies by HTML5 Rocks (free)",
                "Socket.IO Documentation and Tutorial (free)",
                "Server-Sent Events by MDN (free)",
                "Firebase Documentation (free)",
                "Real-time Systems Course by MIT (free)"
            ],
            "Free Search & Analytics Resources": [
                "Elasticsearch Official Documentation (free)",
                "Elastic Stack Tutorial by Elastic (free)",
                "Apache Kafka Documentation (free)",
                "ELK Stack Tutorial by Digital Ocean (free)",
                "Data Engineering Course by DataTalks.Club (free)",
                "Log Analysis Tutorial by Splunk (free tier)"
            ]
        }
    },

    "Phase 9: DevOps & Infrastructure": {
        "duration": "3-4 months",
        "topics": {
            "Containerization & Orchestration": [
                "Docker deep dive",
                "Kubernetes fundamentals",
                "Helm charts",
                "Service mesh (Istio)",
                "Container security",
                "Container registry management"
            ],
            "CI/CD Pipelines": [
                "Jenkins/GitHub Actions/GitLab CI",
                "Automated testing in CI/CD",
                "Blue-green deployments",
                "Canary releases",
                "Infrastructure as Code",
                "Pipeline security and compliance"
            ],
            "Monitoring & Logging": [
                "Prometheus and Grafana",
                "ELK Stack (Elasticsearch, Logstash, Kibana)",
                "APM tools (New Relic, DataDog)",
                "Distributed tracing",
                "Error tracking (Sentry)",
                "Log management and analysis"
            ],
            "Cloud Native": [
                "Serverless architectures",
                "Function as a Service (FaaS)",
                "API Gateway",
                "Cloud databases",
                "Auto-scaling strategies",
                "Multi-cloud and hybrid cloud strategies"
            ]
        },
        "resources": {
            "Free Docker & Kubernetes": [
                "Docker Official Documentation (free)",
                "Play with Docker (free hands-on playground)",
                "Kubernetes Official Documentation (free)",
                "Kubernetes Course by freeCodeCamp (YouTube - 4+ hours)",
                "Docker and Kubernetes by TechWorld with Nana (YouTube)",
                "Katacoda Interactive Learning (free tier)"
            ],
            "Free CI/CD Resources": [
                "GitHub Actions Documentation (free)",
                "GitLab CI Documentation (free tier)",
                "Jenkins Official Documentation (free)",
                "DevOps Course by freeCodeCamp (YouTube)",
                "CI/CD Pipeline Tutorial by TechWorld with Nana (YouTube)",
                "Azure DevOps Learning Path (free)"
            ],
            "Free Monitoring Resources": [
                "Prometheus Official Documentation (free)",
                "Grafana Documentation and Tutorials (free)",
                "ELK Stack Documentation by Elastic (free)",
                "Monitoring and Observability by Google (free course)",
                "Site Reliability Engineering by Google (free book)",
                "Datadog Learning Center (free resources)"
            ],
            "Free Cloud Native Resources": [
                "CNCF (Cloud Native Computing Foundation) resources (free)",
                "Serverless Framework Documentation (free)",
                "AWS Lambda Documentation (free)",
                "Cloud Native Course by CNCF (free)",
                "Istio Service Mesh Documentation (free)",
                "OpenFaaS Documentation (free)"
            ]
        }
    },

    "Phase 10: Specialization Tracks": {
        "duration": "4-6 months (choose one)",
        "topics": {
            "Full-Stack Development": [
                "Advanced React patterns",
                "Server-side rendering optimization",
                "Progressive Web Apps (PWA)",
                "Mobile app development (React Native/Flutter)",
                "Micro-frontends"
            ],
            "Backend Engineering": [
                "High-performance computing",
                "Stream processing (Apache Kafka, Flink)",
                "Big data technologies (Hadoop, Spark)",
                "Machine learning integration",
                "Blockchain basics"
            ],
            "Platform Engineering": [
                "Platform as a Service design",
                "Developer experience optimization",
                "Internal tooling development",
                "Service catalog creation",
                "Golden path templates"
            ],
            "Security Engineering": [
                "Penetration testing",
                "Security auditing",
                "Cryptography implementation",
                "Zero-trust architecture",
                "Compliance (GDPR, HIPAA)"
            ],
            "Data Engineering": [
                "Data pipeline design",
                "Apache Spark and Hadoop ecosystem",
                "Real-time data processing",
                "Data lake and data warehouse architecture",
                "ETL/ELT optimization"
            ]
        },
        "resources": {
            "Full-Stack Specialization (Free)": [
                "Advanced React by Epic React (free articles)",
                "Next.js Documentation and Learn Course (free)",
                "Progressive Web Apps by Google (free course)",
                "React Native Documentation and Tutorial (free)",
                "Flutter Documentation and Codelabs (free)",
                "Micro-frontends by Martin Fowler (free articles)"
            ],
            "Backend Engineering (Free)": [
                "Apache Kafka Documentation (free)",
                "Apache Spark Documentation (free)",
                "Big Data Course by DataTalks.Club (free)",
                "Machine Learning by Andrew Ng (Coursera - audit free)",
                "Blockchain Basics by IBM (free course)",
                "High Performance Computing by LLNL (free tutorials)"
            ],
            "Security Engineering (Free)": [
                "OWASP WebGoat (free security testing)",
                "Cybersecurity Course by freeCodeCamp (YouTube)",
                "Penetration Testing by SANS (free resources)",
                "Cryptography by Stanford (Coursera - audit free)",
                "Security by Design by OWASP (free)",
                "Web Security Academy by PortSwigger (free)"
            ],
            "Data Engineering (Free)": [
                "Data Engineering Course by DataTalks.Club (free)",
                "Apache Airflow Documentation (free)",
                "Apache Kafka Streams Tutorial (free)",
                "Data Engineering on GCP (free tier)",
                "Spark by Example (free tutorials)",
                "Data Warehousing by Snowflake (free tier and resources)"
            ]
        }
    },

    "Phase 11: Senior Engineering Skills": {
        "duration": "Ongoing",
        "topics": {
            "Technical Leadership": [
                "Technical decision making",
                "Architecture documentation (ADRs)",
                "Mentoring junior developers",
                "Code review mastery",
                "Technical debt management"
            ],
            "Soft Skills": [
                "Communication with stakeholders",
                "Project estimation",
                "Conflict resolution",
                "Team collaboration",
                "Presentation skills"
            ],
            "Business Acumen": [
                "Understanding business metrics",
                "Cost optimization",
                "ROI analysis",
                "Product thinking",
                "Customer empathy"
            ],
            "Continuous Learning": [
                "Staying current with technology",
                "Building learning habits",
                "Conference participation",
                "Open source contribution",
                "Technical writing"
            ]
        },
        "resources": {
            "Free Leadership Resources": [
                "Engineering Management by Will Larson (free articles)",
                "The Manager's Path - selected chapters (free)",
                "Technical Leadership by Patrick Kua (free articles)",
                "Google's Engineering Practices (free documentation)",
                "Tech Lead Wisdom by Patrick Kua (free resources)",
                "Engineering Leadership by Honeycomb (free articles)"
            ],
            "Free Communication & Soft Skills": [
                "Technical Writing by Google (free course)",
                "Communication for Engineers by MIT (free resources)",
                "Presentation Skills by Coursera (audit free)",
                "Conflict Resolution by Harvard Business Review (free articles)",
                "Team Collaboration by Atlassian (free guides)",
                "Public Speaking by Toastmasters (free resources)"
            ],
            "Free Business Acumen Resources": [
                "Business Model Canvas by Strategyzer (free template)",
                "Lean Startup Methodology (free resources)",
                "Product Management by Google (free course)",
                "Business Metrics by HubSpot Academy (free)",
                "ROI Analysis by CFI (free tutorials)",
                "Customer Development by Steve Blank (free articles)"
            ],
            "Free Continuous Learning": [
                "Open Source Friday by GitHub (free)",
                "DEV Community (free platform for technical writing)",
                "Tech Conference YouTube channels (free talks)",
                "Hacker News (free tech news and discussions)",
                "Reddit Programming communities (free)",
                "Medium Engineering blogs (free tier)",
                "GitHub Trending repositories (free inspiration)"
            ]
        }
    }

    # Additional Free Resources (for reference):
    # 
    # Comprehensive Learning Platforms:
    # - freeCodeCamp.org - Full stack certification tracks (completely free)
    # - The Odin Project - Complete web development curriculum (free)
    # - Coursera - Audit courses from top universities (free)
    # - edX - University courses and certifications (free audit)
    # - MIT OpenCourseWare - Complete MIT courses (free)
    # - Khan Academy - Computer Science and Programming (free)
    #
    # Top YouTube Channels for Software Engineering:
    # - freeCodeCamp.org - Comprehensive programming courses
    # - Programming with Mosh - Clean, professional tutorials
    # - The Net Ninja - Web development and frameworks
    # - Traversy Media - Practical web development
    # - Academind - React, Node.js, and modern web dev
    # - CS Dojo - Computer science and programming concepts
    # - TechWorld with Nana - DevOps and cloud technologies
    # - Hussein Nasser - Backend engineering and databases
    # - Gaurav Sen - System design interviews
    # - ByteByteGo - System design and architecture
    #
    # Free Practice Platforms:
    # - LeetCode - Algorithm and data structure problems (free tier)
    # - HackerRank - Programming challenges across domains (free)
    # - CodeSignal - Coding practice and assessments (free tier)
    # - Codeforces - Competitive programming (free)
    # - AtCoder - Algorithm contests (free)
    # - TopCoder - Programming competitions (free)
    # - GeeksforGeeks - Programming problems and tutorials (free)
    # - InterviewBit - Technical interview preparation (free tier)
    #
    # Free Tools & IDEs:
    # - Visual Studio Code - Free, extensible code editor
    # - Git - Free version control system
    # - Docker Desktop - Free containerization (personal use)
    # - Postman - Free API development and testing
    # - DBeaver - Free database management tool
    # - Figma - Free UI/UX design tool
    # - draw.io - Free diagramming tool
    #
    # Free Cloud Tiers:
    # - AWS Free Tier - 12 months of selected services
    # - Google Cloud Free Tier - Always free and trial credits
    # - Microsoft Azure Free Tier - 12 months plus always free services
    # - Heroku - Free tier for small applications
    # - Netlify - Free hosting for static sites
    # - Vercel - Free hosting for frontend applications
    # - Firebase - Free tier for mobile and web apps
    # - MongoDB Atlas - Free tier for database hosting
}




ML_RESEARCH_ROADMAP = {
    
    "Phase 1: Mathematical Foundations": {
        "duration": "3-4 months",
        "prerequisites": "High school mathematics",
        "topics": {
            "Linear Algebra": [
                "Vectors, matrices, eigenvalues, eigenvectors",
                "Matrix decompositions (SVD, PCA)",
                "LLM-specific: Understanding attention as matrix operations",
                "CV-specific: Understanding convolutions as matrix operations"
            ],
            "Calculus & Optimization": [
                "Derivatives, partial derivatives, chain rule",
                "Gradients, Hessians",
                "Convex optimization basics",
                "LLM-specific: Understanding gradient flow in transformer training",
                "CV-specific: Understanding backpropagation in CNNs"
            ],
            "Statistics & Probability": [
                "Probability distributions, Bayes' theorem",
                "Hypothesis testing, confidence intervals",
                "Maximum likelihood estimation",
                "LLM-specific: Language modeling as probability estimation",
                "CV-specific: Understanding uncertainty in vision tasks"
            ],
            "Information Theory": [
                "Entropy, mutual information",
                "Cross-entropy loss intuition"
            ]
        },
        "resources": {
            "Courses": [
                "Mathematics for Machine Learning (Coursera)",
                "Linear Algebra - MIT OCW",
                "Statistical Learning - Stanford"
            ],
            "Books": [
                "Pattern Recognition and Machine Learning - Bishop",
                "The Elements of Statistical Learning",
                "Deep Learning - Ian Goodfellow (Part 1)"
            ]
        }
    },

    "Phase 2: Programming & Tools": {
        "duration": "2-3 months",
        "prerequisites": "Phase 1 completion",
        "topics": {
            "Python Mastery": [
                "Data structures, OOP, functional programming",
                "NumPy, Pandas, Matplotlib, Seaborn",
                "Jupyter notebooks, debugging"
            ],
            "Machine Learning Libraries": [
                "Scikit-learn for traditional ML",
                "PyTorch (preferred for both LLM and CV research)",
                "CV libraries: OpenCV, PIL/Pillow, scikit-image",
                "LLM libraries: HuggingFace Transformers, tokenizers"
            ],
            "Specialized Tools": [
                "For CV: Albumentations, YOLO, detectron2",
                "For LLM: HuggingFace ecosystem, DeepSpeed, vLLM",
                "Common: Weights & Biases for experiment tracking"
            ],
            "Development Tools": [
                "Git/GitHub for version control",
                "Command line proficiency",
                "Docker basics",
                "Cloud platforms with GPU support (AWS, GCP, Azure)"
            ]
        },
        "resources": {
            "Courses": [
                "Python for Data Science - Coursera",
                "PyTorch Fundamentals - PyTorch.org",
                "Practical Deep Learning - fast.ai"
            ],
            "Books": [
                "Hands-On Machine Learning - Aurélien Géron",
                "Programming PyTorch for Deep Learning"
            ]
        }
    },

    "Phase 3: Core Machine Learning": {
        "duration": "4-5 months",
        "prerequisites": "Phases 1-2 completion",
        "topics": {
            "Traditional ML Concepts": [
                "Linear/logistic regression",
                "Decision trees, random forests",
                "Support vector machines",
                "Clustering: K-means, hierarchical",
                "Dimensionality reduction: PCA, t-SNE"
            ],
            "Data Processing": [
                "Data cleaning and preprocessing",
                "Feature engineering principles",
                "For CV: Image preprocessing, augmentation techniques",
                "For LLM: Text preprocessing, tokenization basics",
                "Handling missing data and outliers"
            ],
            "Model Evaluation & Selection": [
                "Cross-validation techniques",
                "Bias-variance tradeoff",
                "Regularization techniques (L1, L2)",
                "CV metrics: Accuracy, Precision, Recall, F1, IoU, mAP",
                "LLM metrics: BLEU, ROUGE, perplexity, BERTScore"
            ]
        },
        "resources": {
            "Courses": [
                "Machine Learning - Andrew Ng (Coursera)",
                "CS229 - Stanford Machine Learning"
            ],
            "Books": [
                "An Introduction to Statistical Learning",
                "Machine Learning Yearning - Andrew Ng"
            ]
        }
    },

    "Phase 4: Deep Learning Fundamentals": {
        "duration": "3-4 months",
        "prerequisites": "Phase 3 completion",
        "topics": {
            "Neural Network Fundamentals": [
                "Perceptrons and multilayer perceptrons",
                "Backpropagation algorithm",
                "Activation functions (ReLU, sigmoid, tanh, etc.)",
                "Loss functions (MSE, cross-entropy, etc.)",
                "Gradient descent variants (SGD, Adam, AdamW)"
            ],
            "Core Architectures": [
                "Feedforward networks",
                "Convolutional Neural Networks (CNNs) - essential for CV",
                "Recurrent Neural Networks (RNNs, LSTMs, GRUs) - foundation for LLMs"
            ],
            "Advanced Topics": [
                "Transfer learning concepts",
                "Regularization techniques (dropout, batch norm)",
                "Advanced optimizers and learning rate scheduling",
                "Initialization strategies"
            ]
        },
        "resources": {
            "Courses": [
                "Deep Learning Specialization - Andrew Ng",
                "CS231n - Stanford CNN for Visual Recognition"
            ],
            "Books": [
                "Deep Learning - Goodfellow, Bengio, Courville"
            ]
        }
    },

    "Phase 5: Foundation Specialization (Choose Path)": {
        "duration": "3-4 months",
        "prerequisites": "Phase 4 completion",
        "note": "Choose either Computer Vision OR NLP track, or do both sequentially",
        "topics": {
            "Option A: Computer Vision Foundation": [
                "Image fundamentals: pixels, channels, color spaces",
                "Basic operations: filtering, edge detection, morphological operations",
                "Feature extraction: SIFT, SURF, HOG",
                "Classical techniques: template matching, contour detection",
                "Image classification basics with CNNs"
            ],
            "Option B: NLP Foundation": [
                "Classical NLP: n-grams, POS tagging, NER",
                "Word embeddings: Word2Vec, GloVe, FastText",
                "Sequence models: basic RNNs for text",
                "Text preprocessing: tokenization, normalization",
                "Sentiment analysis and text classification"
            ]
        },
        "resources": {
            "Courses": [
                "CS231n - Stanford Computer Vision",
                "CS224N - Stanford NLP with Deep Learning"
            ],
            "Books": [
                "Computer Vision: Algorithms and Applications - Szeliski",
                "Speech and Language Processing - Jurafsky & Martin"
            ]
        }
    },

    "Phase 6: Advanced Deep Learning Architectures": {
        "duration": "4-6 months",
        "prerequisites": "Phase 5 completion",
        "topics": {
            "Computer Vision Track - CNN Architectures": [
                "Historical progression: LeNet, AlexNet, VGG",
                "Modern architectures: ResNet, Inception, DenseNet",
                "Efficient architectures: MobileNet, EfficientNet",
                "Vision Transformers (ViTs) and hybrid approaches"
            ],
            "Computer Vision Track - Specialized CV Tasks": [
                "Image Classification: Multi-class, multi-label",
                "Object Detection: R-CNN family, YOLO, SSD, RetinaNet",
                "Semantic Segmentation: U-Net, DeepLab, Mask R-CNN",
                "Instance Segmentation: Mask R-CNN, SOLO"
            ],
            "LLM Track - Transformer Architecture": [
                "Attention mechanisms deep dive",
                "Self-attention vs cross-attention",
                "Encoder-decoder structure",
                "Positional encodings",
                "Implementation from scratch"
            ],
            "LLM Track - Large Language Models": [
                "GPT series evolution (GPT-1 to GPT-4)",
                "BERT and bidirectional models",
                "T5, PaLM, LLaMA architectures",
                "Parameter-efficient fine-tuning (LoRA, Adapters)"
            ]
        },
        "resources": {
            "Courses": [
                "Transformers Course - HuggingFace",
                "Advanced Computer Vision - Coursera"
            ],
            "Papers": [
                "Attention Is All You Need",
                "BERT, GPT papers series",
                "ResNet, Vision Transformer papers"
            ]
        }
    },

    "Phase 7: Reinforcement Learning Fundamentals": {
        "duration": "3-4 months",
        "prerequisites": "Phase 6 completion",
        "topics": {
            "Core RL Concepts": [
                "Markov Decision Processes (MDPs)",
                "Value functions, policy functions",
                "Bellman equations and dynamic programming",
                "Exploration vs exploitation trade-off"
            ],
            "Classical RL Algorithms": [
                "Q-Learning, SARSA",
                "Policy gradient methods",
                "Temporal difference learning",
                "Monte Carlo methods"
            ],
            "Deep Reinforcement Learning": [
                "Deep Q-Networks (DQN) and variants",
                "Actor-Critic methods (A2C, A3C)",
                "Proximal Policy Optimization (PPO)",
                "Deep Deterministic Policy Gradient (DDPG)"
            ],
            "Advanced RL Topics": [
                "Multi-agent reinforcement learning",
                "Hierarchical reinforcement learning",
                "Inverse reinforcement learning",
                "RLHF (Reinforcement Learning from Human Feedback)"
            ]
        },
        "resources": {
            "Courses": [
                "CS285 - UC Berkeley Deep RL",
                "Reinforcement Learning Specialization - University of Alberta",
                "DeepMind RL Course"
            ],
            "Books": [
                "Reinforcement Learning: An Introduction - Sutton & Barto",
                "Deep Reinforcement Learning Hands-On - Maxim Lapan"
            ],
            "Libraries": [
                "OpenAI Gym, Gymnasium",
                "Stable Baselines3",
                "Ray RLlib",
                "TensorFlow Agents"
            ]
        }
    },

    "Phase 8: Multimodal AI Systems": {
        "duration": "4-5 months",
        "prerequisites": "Phase 7 completion, some CV and NLP background",
        "topics": {
            "Audio Processing & Speech AI": [
                "Digital signal processing basics",
                "Speech Recognition (ASR): Whisper, Wav2Vec2",
                "Speech Synthesis (TTS): Tacotron, WaveNet, modern TTS",
                "Audio understanding and classification"
            ],
            "Video Processing & Understanding": [
                "Video fundamentals and temporal modeling",
                "Action recognition: 3D CNNs, Video Transformers",
                "Video object detection and tracking",
                "Video generation and editing"
            ],
            "Vision-Language Models": [
                "CLIP and its variants",
                "DALL-E, Stable Diffusion",
                "GPT-4V, LLaVA, multimodal understanding",
                "Text-to-image and image-to-text generation"
            ],
            "Cross-Modal Learning": [
                "Audio-visual synchronization",
                "Multimodal fusion techniques",
                "Cross-modal retrieval",
                "Unified multimodal architectures"
            ]
        },
        "resources": {
            "Libraries": [
                "librosa, torchaudio (audio)",
                "OpenCV, MoviePy (video)",
                "HuggingFace multimodal models",
                "OpenAI CLIP, Stability AI models"
            ],
            "Papers": [
                "CLIP, ALIGN, Flamingo",
                "DALL-E series, Stable Diffusion",
                "Whisper, recent multimodal papers"
            ]
        }
    },

    "Phase 9: Advanced AI Techniques": {
        "duration": "4-5 months",
        "prerequisites": "Phase 8 completion",
        "topics": {
            "Retrieval-Augmented Generation (RAG)": [
                "Information retrieval basics",
                "Vector databases and similarity search",
                "RAG architecture and components",
                "Advanced RAG: multi-hop, self-RAG"
            ],
            "Advanced Training Techniques": [
                "Self-supervised learning",
                "Few-shot and meta-learning",
                "Domain adaptation and transfer learning",
                "Continual learning and catastrophic forgetting"
            ],
            "Model Optimization": [
                "Neural Architecture Search (NAS)",
                "Knowledge distillation",
                "Pruning and quantization",
                "Distributed training strategies"
            ],
            "Safety and Interpretability": [
                "Adversarial examples and robustness",
                "Explainable AI: LIME, SHAP, Grad-CAM",
                "Bias detection and fairness",
                "AI alignment principles"
            ]
        },
        "resources": {
            "Tools & Libraries": [
                "LangChain, LlamaIndex (RAG)",
                "Chroma, Pinecone, FAISS (vector stores)",
                "Ray for distributed computing",
                "Interpretability libraries"
            ],
            "Papers": [
                "RAG, DPR papers",
                "Self-supervised learning papers",
                "Interpretability and safety papers"
            ]
        }
    },

    "Phase 10: Agentic AI & Advanced Applications": {
        "duration": "4-5 months",
        "prerequisites": "Phase 9 completion",
        "topics": {
            "Agentic AI Systems": [
                "Agent architecture and planning",
                "ReAct (Reasoning + Acting)",
                "Tool use and function calling",
                "Multi-agent systems and coordination"
            ],
            "Model Communication Protocol (MCP)": [
                "MCP server development",
                "Custom tool integration",
                "API orchestration patterns",
                "Security and best practices"
            ],
            "Advanced Applications": [
                "Code generation systems",
                "Scientific AI applications",
                "Creative AI and content generation",
                "Embodied AI and robotics integration"
            ],
            "Agent Safety & Control": [
                "Goal alignment and containment",
                "Human oversight integration",
                "Robustness testing for agents",
                "Multi-agent coordination safety"
            ]
        },
        "resources": {
            "Frameworks": [
                "LangGraph, CrewAI",
                "AutoGen, OpenAI Assistants API",
                "MCP SDK libraries",
                "Custom agent implementations"
            ],
            "Papers": [
                "ReAct, Toolformer",
                "Agent-based papers",
                "Tool-use papers"
            ]
        }
    },

    "Phase 11: Edge AI & Mobile Deployment": {
        "duration": "3-4 months",
        "prerequisites": "Phase 10 completion",
        "topics": {
            "Model Optimization for Edge": [
                "Quantization: INT8, INT4, binary networks",
                "Pruning: structured and unstructured",
                "Knowledge distillation for efficiency",
                "Neural architecture search for mobile"
            ],
            "Mobile AI Frameworks": [
                "TensorFlow Lite, TensorFlow.js",
                "Core ML (iOS), ML Kit (Android)",
                "ONNX Runtime, OpenVINO",
                "PyTorch Mobile, MediaPipe"
            ],
            "Hardware-Specific Optimization": [
                "CPU optimization (NEON, AVX)",
                "GPU optimization (Metal, OpenCL)",
                "NPU/TPU utilization",
                "Memory management constraints"
            ],
            "Real-world Deployment": [
                "Real-time processing requirements",
                "Battery and thermal considerations",
                "Offline capabilities",
                "AR/VR and IoT applications"
            ]
        },
        "resources": {
            "Tools": [
                "TensorFlow Lite Converter",
                "Core ML Tools",
                "ONNX optimization tools",
                "Mobile profiling and benchmarking tools"
            ]
        }
    },

    "Phase 12: Research Skills & Paper Implementation": {
        "duration": "4-6 months",
        "prerequisites": "Phase 11 completion",
        "topics": {
            "Research Paper Reading": [
                "Foundational papers: Transformer, ResNet, etc.",
                "Recent breakthrough papers",
                "Conference venues: NeurIPS, ICML, ICLR, CVPR, ACL",
                "Critical evaluation of research claims"
            ],
            "Implementation Projects": [
                "Reproduce 3-4 papers from scratch",
                "Create novel combinations of techniques",
                "Build end-to-end applications",
                "Open-source contributions"
            ],
            "Research Methodology": [
                "Experimental design and hypothesis testing",
                "Statistical significance and reproducibility",
                "Writing technical reports",
                "Peer review process"
            ],
            "Domain Specialization Projects": [
                "Choose 2-3 application domains",
                "Medical AI, Finance AI, or Scientific AI",
                "Creative AI, Industrial AI, or Climate AI",
                "Build domain-specific expertise"
            ]
        },
        "resources": {
            "Paper Resources": [
                "Papers with Code",
                "arXiv.org and conference proceedings",
                "Annotated paper implementations",
                "Research group collaborations"
            ]
        }
    },

    "Phase 13: Production AI Systems & MLOps": {
        "duration": "4-5 months",
        "prerequisites": "Phase 12 completion",
        "topics": {
            "MLOps Fundamentals": [
                "Model versioning and registry",
                "CI/CD for ML pipelines",
                "Automated testing for ML systems",
                "Model monitoring and drift detection"
            ],
            "Scalable Infrastructure": [
                "Distributed training systems",
                "Model serving architectures",
                "Auto-scaling and load balancing",
                "Cost optimization strategies"
            ],
            "Production Safety": [
                "A/B testing for model deployment",
                "Canary releases and rollback strategies",
                "Bias monitoring in production",
                "Privacy-preserving deployment"
            ],
            "Enterprise Integration": [
                "API design for AI services",
                "Real-time vs batch processing",
                "Multi-model orchestration",
                "Compliance and governance frameworks"
            ]
        },
        "resources": {
            "Platforms": [
                "Kubernetes, Docker",
                "MLflow, Kubeflow, Weights & Biases",
                "Cloud ML platforms (AWS SageMaker, GCP Vertex AI, Azure ML)",
                "Monitoring tools (Grafana, Prometheus)"
            ],
            "Books": [
                "Building Machine Learning Powered Applications",
                "ML Engineering - Andriy Burkov",
                "Reliable Machine Learning"
            ]
        }
    },

    "Phase 14: Ethics & Responsible AI": {
        "duration": "2-3 months",
        "prerequisites": "Phase 13 completion",
        "topics": {
            "AI Ethics Framework": [
                "Bias and fairness in ML systems",
                "Algorithmic transparency and accountability",
                "Privacy-preserving ML techniques",
                "Environmental impact of AI systems"
            ],
            "Regulatory Compliance": [
                "GDPR and data protection",
                "AI Act and emerging regulations",
                "Industry-specific compliance",
                "Audit trails and documentation"
            ],
            "Safety Testing": [
                "Red teaming and adversarial testing",
                "Robustness evaluation",
                "Failure mode analysis",
                "Human oversight integration"
            ]
        },
        "resources": {
            "Guidelines": [
                "Partnership on AI principles",
                "IEEE Standards for AI",
                "Responsible AI frameworks from major tech companies"
            ]
        }
    },

    "Phase 15: Cutting-Edge Research & Future Technologies": {
        "duration": "6+ months",
        "prerequisites": "Phase 14 completion",
        "topics": {
            "Quantum Machine Learning": [
                "Quantum computing basics for ML",
                "Variational quantum algorithms",
                "Quantum neural networks",
                "Near-term quantum advantage"
            ],
            "Emerging AI Paradigms": [
                "Neuromorphic computing",
                "In-memory computing for AI",
                "Brain-computer interfaces",
                "Biological-inspired AI architectures"
            ],
            "Research Leadership": [
                "Leading research teams",
                "Grant writing and funding",
                "Conference organization",
                "Industry-academia collaboration"
            ],
            "Original Research Contribution": [
                "Novel algorithm development",
                "Theoretical contributions",
                "Large-scale empirical studies",
                "Publication in top-tier venues"
            ]
        },
        "resources": {
            "Research Communities": [
                "Academic conferences and workshops",
                "Research collaborations",
                "Open-source project leadership",
                "Industry research partnerships"
            ]
        }
    }
}

QUANT_RESEARCH_ROADMAP = {
    "Phase 1: Mathematical Foundations": {
        "duration": "4-6 months",
        "topics": {
            "Calculus & Real Analysis": [
                "Multivariable calculus, partial derivatives",
                "Taylor series, optimization theory",
                "Measure theory basics",
                "Ito calculus fundamentals for stochastic processes"
            ],
            "Linear Algebra": [
                "Matrix operations, eigenvalues, eigenvectors",
                "Principal Component Analysis (PCA)",
                "Singular Value Decomposition (SVD)",
                "Applications in portfolio optimization and risk modeling"
            ],
            "Probability Theory": [
                "Probability spaces, random variables, distributions",
                "Conditional probability, Bayes' theorem",
                "Law of large numbers, central limit theorem",
                "Moment generating functions, characteristic functions"
            ],
            "Statistics": [
                "Hypothesis testing, confidence intervals",
                "Maximum likelihood estimation, method of moments",
                "Regression analysis (linear, logistic, nonlinear)",
                "Time series basics: stationarity, autocorrelation"
            ]
        },
        "resources": {
            "Courses": [
                "Mathematics for Machine Learning - Coursera",
                "Probability Theory - MIT OCW",
                "Statistical Inference - Duke University"
            ],
            "Books": [
                "Introduction to Mathematical Statistics - Hogg & Craig",
                "Probability and Measure - Billingsley",
                "Linear Algebra and Its Applications - Strang"
            ]
        }
    },
    "Phase 2: Programming & Technical Tools": {
        "duration": "3-4 months",
        "topics": {
            "Python for Finance": [
                "NumPy, Pandas, Matplotlib, Seaborn",
                "Financial libraries: QuantLib, yfinance, pandas_datareader",
                "Data manipulation and cleaning techniques",
                "Object-oriented programming for financial modeling"
            ],
            "R Programming": [
                "Data analysis with R",
                "Financial packages: quantmod, PerformanceAnalytics, tidyquant",
                "Statistical modeling and visualization",
                "R Shiny for interactive dashboards"
            ],
            "Database & Data Management": [
                "SQL for financial data queries",
                "Time series databases: InfluxDB, TimescaleDB",
                "Bloomberg API, Reuters/Refinitiv APIs",
                "Alternative data sources and APIs"
            ],
            "Performance Computing": [
                "C++ basics for high-frequency trading",
                "Parallel computing with Python multiprocessing",
                "GPU computing for Monte Carlo simulations",
                "Memory optimization and vectorization"
            ]
        },
        "resources": {
            "Courses": [
                "Python for Financial Analysis - Udemy",
                "R Programming for Finance - DataCamp",
                "Bloomberg Terminal Training"
            ],
            "Books": [
                "Python for Finance - Yves Hilpisch",
                "R for Data Science - Wickham & Grolemund",
                "Financial Instrument Pricing Using C++ - Duffy"
            ]
        }
    },
    "Phase 3: Financial Theory & Markets": {
        "duration": "4-5 months",
        "topics": {
            "Financial Markets Structure": [
                "Equity, fixed income, derivatives, commodities markets",
                "Market microstructure, bid-ask spreads, liquidity",
                "High-frequency trading, algorithmic trading",
                "Regulatory environment and compliance"
            ],
            "Corporate Finance": [
                "Time value of money, present value calculations",
                "Capital structure, cost of capital",
                "Dividend discount models, DCF analysis",
                "Financial statement analysis"
            ],
            "Investment Theory": [
                "Modern Portfolio Theory (MPT)",
                "Capital Asset Pricing Model (CAPM)",
                "Arbitrage Pricing Theory (APT)",
                "Efficient Market Hypothesis and behavioral finance"
            ],
            "Fixed Income": [
                "Bond pricing, yield calculations",
                "Duration, convexity, immunization",
                "Term structure models",
                "Credit risk and default probability"
            ]
        },
        "resources": {
            "Courses": [
                "Financial Markets - Yale (Coursera)",
                "Introduction to Corporate Finance - Wharton",
                "Fixed Income Securities - MIT"
            ],
            "Books": [
                "Investments - Bodie, Kane, Marcus",
                "Corporate Finance - Ross, Westerfield, Jaffe",
                "Fixed Income Securities - Tuckman & Serrat"
            ]
        }
    },
    "Phase 4: Stochastic Processes & Mathematical Finance": {
        "duration": "5-6 months",
        "topics": {
            "Stochastic Processes": [
                "Random walks, Brownian motion",
                "Geometric Brownian motion for stock prices",
                "Ito's lemma and stochastic differential equations",
                "Jump processes, Poisson processes"
            ],
            "Derivatives Pricing": [
                "Black-Scholes-Merton model derivation",
                "Greeks: Delta, Gamma, Theta, Vega, Rho",
                "Exotic options pricing",
                "American options and early exercise"
            ],
            "Risk-Neutral Valuation": [
                "Risk-neutral probability measures",
                "Martingales in finance",
                "Change of measure techniques",
                "Monte Carlo simulation methods"
            ],
            "Interest Rate Models": [
                "Vasicek, CIR, Hull-White models",
                "Heath-Jarrow-Morton framework",
                "LIBOR market models",
                "Bond and interest rate derivatives"
            ]
        },
        "resources": {
            "Courses": [
                "Stochastic Processes - MIT OCW",
                "Mathematical Finance - Stanford",
                "Derivatives Pricing - NYU Stern"
            ],
            "Books": [
                "Stochastic Calculus for Finance I & II - Shreve",
                "Options, Futures, and Other Derivatives - Hull",
                "Methods of Mathematical Finance - Karatzas & Shreve"
            ]
        }
    },
    "Phase 5: Risk Management & Portfolio Theory": {
        "duration": "4-5 months",
        "topics": {
            "Portfolio Optimization": [
                "Mean-variance optimization",
                "Black-Litterman model",
                "Risk parity and equal risk contribution",
                "Multi-factor models and factor investing"
            ],
            "Risk Metrics": [
                "Value at Risk (VaR): Historical, parametric, Monte Carlo",
                "Expected Shortfall (Conditional VaR)",
                "Maximum Drawdown, Sharpe ratio, Sortino ratio",
                "Risk attribution and decomposition"
            ],
            "Credit Risk": [
                "Probability of default modeling",
                "Loss given default estimation",
                "Credit portfolio models",
                "Stress testing and scenario analysis"
            ],
            "Market Risk": [
                "Factor models: Fama-French, Carhart",
                "GARCH models for volatility",
                "Copulas for dependency modeling",
                "Backtesting and model validation"
            ]
        },
        "resources": {
            "Courses": [
                "Risk Management - NYU Stern",
                "Portfolio Management - EDHEC",
                "Financial Risk Manager (FRM) - GARP"
            ],
            "Books": [
                "The Concepts and Practice of Mathematical Finance - Joshi",
                "Portfolio Selection - Markowitz",
                "Value at Risk - Jorion"
            ]
        }
    },
    "Phase 6: Quantitative Trading Strategies": {
        "duration": "4-6 months",
        "topics": {
            "Statistical Arbitrage": [
                "Pairs trading, cointegration",
                "Mean reversion strategies",
                "Statistical significance and p-hacking",
                "Transaction costs and market impact"
            ],
            "Momentum & Trend Following": [
                "Technical indicators and signals",
                "Cross-sectional and time-series momentum",
                "Risk management in trending markets",
                "Regime detection and switching models"
            ],
            "Market Making": [
                "Optimal bid-ask spread setting",
                "Inventory risk management",
                "Adverse selection and information asymmetry",
                "High-frequency market making strategies"
            ],
            "Factor Investing": [
                "Value, quality, momentum, low volatility factors",
                "Factor construction and backtesting",
                "Multi-factor model implementation",
                "Factor timing and allocation"
            ]
        },
        "resources": {
            "Courses": [
                "Algorithmic Trading - Stanford",
                "Quantitative Trading Strategies - Coursera",
                "CQF (Certificate in Quantitative Finance)"
            ],
            "Books": [
                "Quantitative Trading - Ernest Chan",
                "Algorithmic Trading - Stefan Jansen",
                "Finding Alphas - Tulchinsky et al."
            ]
        }
    },
    "Phase 7: Machine Learning in Finance": {
        "duration": "5-6 months",
        "topics": {
            "Traditional ML for Finance": [
                "Linear/logistic regression for return prediction",
                "Random forests for feature selection",
                "Support Vector Machines for classification",
                "Principal Component Analysis for dimensionality reduction"
            ],
            "Time Series Forecasting": [
                "ARIMA, GARCH models",
                "Vector Autoregression (VAR)",
                "Long Short-Term Memory (LSTM) networks",
                "Transformer models for financial sequences"
            ],
            "Alternative Data & NLP": [
                "Sentiment analysis from news and social media",
                "Natural Language Processing for earnings calls",
                "Satellite data, credit card transactions",
                "Web scraping and alternative data sources"
            ],
            "Reinforcement Learning": [
                "Q-learning for trading strategies",
                "Policy gradient methods",
                "Multi-agent systems in markets",
                "Portfolio optimization with RL"
            ]
        },
        "resources": {
            "Courses": [
                "Machine Learning for Trading - Georgia Tech",
                "Financial Engineering - Stanford",
                "AI for Trading - Udacity Nanodegree"
            ],
            "Books": [
                "Machine Learning for Algorithmic Trading - Stefan Jansen",
                "Advances in Financial Machine Learning - Marcos López de Prado",
                "Hands-On Machine Learning - Aurélien Géron"
            ]
        }
    },
    "Phase 8: Advanced Quantitative Methods": {
        "duration": "4-6 months",
        "topics": {
            "Systematic Risk Models": [
                "Barra risk models",
                "Axioma factor models",
                "Custom factor construction",
                "Risk forecasting and stress testing"
            ],
            "Execution Algorithms": [
                "TWAP, VWAP algorithms",
                "Implementation Shortfall",
                "Optimal execution theory (Almgren-Chriss)",
                "Market impact models"
            ],
            "Structured Products": [
                "Equity-linked notes, barrier options",
                "Volatility products, variance swaps",
                "Credit derivatives, CDOs",
                "Hybrid products and complex payoffs"
            ],
            "Regulatory & Compliance": [
                "Basel III capital requirements",
                "MiFID II, Dodd-Frank regulations",
                "Model validation and governance",
                "Stress testing frameworks"
            ]
        },
        "resources": {
            "Professional Courses": [
                "Risk Management Professional (PRM)",
                "Chartered Financial Analyst (CFA)",
                "Financial Risk Manager (FRM)"
            ],
            "Industry Publications": [
                "Journal of Portfolio Management",
                "Quantitative Finance",
                "Risk Magazine"
            ]
        }
    },
    "Phase 9: Research & Strategy Development": {
        "duration": "6+ months",
        "topics": {
            "Research Process": [
                "Hypothesis formation and testing",
                "Data mining and feature engineering",
                "Backtesting methodologies and pitfalls",
                "Out-of-sample testing and walk-forward analysis"
            ],
            "Strategy Implementation": [
                "Portfolio construction and optimization",
                "Risk budgeting and allocation",
                "Performance attribution analysis",
                "Transaction cost analysis"
            ],
            "Alternative Strategies": [
                "Cryptocurrency and digital assets",
                "ESG investing and sustainable finance",
                "Volatility trading and VIX strategies",
                "Cross-asset momentum and carry trades"
            ],
            "Research Tools & Platforms": [
                "Bloomberg Terminal, Refinitiv Eikon",
                "FactSet, Morningstar Direct",
                "Academic databases: CRSP, Compustat",
                "Cloud computing for backtesting"
            ]
        },
        "resources": {
            "Research Platforms": [
                "Quantopian (historical), QuantConnect",
                "Alpha Architect, SSRN",
                "Papers from top finance journals"
            ],
            "Industry Conferences": [
                "CFA Institute events",
                "QWAFAFEW, IAQF conferences",
                "Academic finance conferences"
            ]
        }
    },
    "Phase 10: Specialization & Career Development": {
        "duration": "Ongoing",
        "topics": {
            "Career Paths": [
                "Buy-side: Hedge funds, asset management",
                "Sell-side: Investment banks, market making",
                "Risk management: Banks, insurance, consulting",
                "Fintech: Trading platforms, robo-advisors, crypto"
            ],
            "Advanced Specializations": [
                "Systematic trading strategies",
                "Quantitative research and alpha generation",
                "Risk management and model validation",
                "Financial engineering and structuring"
            ],
            "Professional Development": [
                "Industry networking and mentorship",
                "Conference presentations and publications",
                "Open-source contributions to finance libraries",
                "Teaching and knowledge sharing"
            ],
            "Emerging Areas": [
                "DeFi and blockchain applications",
                "Quantum computing in finance",
                "Climate risk and ESG quantification",
                "Central Bank Digital Currencies (CBDCs)"
            ]
        },
        "resources": {
            "Professional Networks": [
                "CFA Institute local societies",
                "IAQF, QWAFAFEW chapters",
                "LinkedIn quantitative finance groups"
            ],
            "Continuous Learning": [
                "Industry publications and blogs",
                "Finance podcasts and webinars",
                "Academic and practitioner conferences"
            ]
        }
    }
}

CS_FRESHER_ROADMAP = {
    "Phase 1: Programming Fundamentals": {
        "duration": "4-6 weeks",
        "topics": {
            "Core Programming Languages": [
                "Java: OOP concepts, collections, exception handling",
                "Python: Data structures, libraries, scripting",
                "C++: Memory management, STL, pointers",
                "JavaScript: ES6+, async programming, DOM manipulation"
            ],
            "Programming Concepts": [
                "Variables, data types, operators",
                "Control structures: loops, conditionals",
                "Functions, recursion, scope",
                "Object-oriented programming: inheritance, polymorphism, encapsulation"
            ],
            "Code Quality": [
                "Clean code principles",
                "Commenting and documentation",
                "Code formatting and style guides",
                "Debugging techniques and tools"
            ],
            "Version Control": [
                "Git fundamentals: commit, push, pull, merge",
                "Branching strategies and conflict resolution",
                "GitHub/GitLab workflows",
                "Collaborative development practices"
            ]
        },
        "resources": {
            "Free Books/PDFs": [
                "Think Java (free PDF)",
                "Automate the Boring Stuff with Python (free online)",
                "Eloquent JavaScript (free online)"
            ],
            "YouTube Channels": [
                "Programming with Mosh",
                "Derek Banas",
                "thenewboston",
                "Coding Train"
            ],
            "Free Websites": [
                "freeCodeCamp.org",
                "Codecademy (free tier)",
                "W3Schools",
                "Oracle Java Documentation"
            ]
        }
    },
    "Phase 2: Data Structures & Algorithms": {
        "duration": "8-10 weeks",
        "topics": {
            "Linear Data Structures": [
                "Arrays: operations, 2D arrays, dynamic arrays",
                "Linked Lists: singly, doubly, circular",
                "Stacks: implementation, applications, expression evaluation",
                "Queues: types, priority queues, deque"
            ],
            "Non-Linear Data Structures": [
                "Trees: binary trees, BST, AVL, heap",
                "Graphs: representation, traversal algorithms",
                "Hash Tables: collision handling, load factor",
                "Tries: prefix trees, string matching"
            ],
            "Algorithm Paradigms": [
                "Divide and Conquer: merge sort, quick sort",
                "Dynamic Programming: memoization, tabulation",
                "Greedy Algorithms: activity selection, Huffman coding",
                "Backtracking: N-Queens, subset generation"
            ],
            "Algorithm Analysis": [
                "Time complexity: Big O, Theta, Omega notation",
                "Space complexity analysis",
                "Best, average, worst case scenarios",
                "Amortized analysis"
            ]
        },
        "resources": {
            "Free Books/PDFs": [
                "Introduction to Algorithms - MIT OCW (free PDF)",
                "Algorithms by Jeff Erickson (free PDF)",
                "Data Structures and Algorithms in Java - free online versions"
            ],
            "YouTube Channels": [
                "Abdul Bari (Algorithms)",
                "mycodeschool",
                "Tushar Roy - Coding Made Simple",
                "Back To Back SWE",
                "William Fiset"
            ],
            "Free Courses": [
                "MIT 6.006 Introduction to Algorithms (YouTube)",
                "Stanford CS106B (YouTube)",
                "freeCodeCamp Algorithms course",
                "Coursera Algorithms (audit for free)"
            ],
            "Free Websites": [
                "GeeksforGeeks",
                "AlgoExpert (some free content)",
                "Programiz",
                "VisuAlgo (algorithm visualization)"
            ]
        }
    },
    "Phase 3: System Design Basics": {
        "duration": "3-4 weeks",
        "topics": {
            "System Architecture": [
                "Client-server architecture",
                "Monolithic vs microservices",
                "Load balancing concepts",
                "Caching strategies (Redis, Memcached)"
            ],
            "Database Fundamentals": [
                "SQL vs NoSQL databases",
                "ACID properties and transactions",
                "Database normalization",
                "Indexing and query optimization"
            ],
            "Scalability Concepts": [
                "Horizontal vs vertical scaling",
                "Database sharding and replication",
                "Content Delivery Networks (CDN)",
                "Message queues and pub-sub systems"
            ],
            "Basic System Design": [
                "URL shortener (like bit.ly)",
                "Chat application design",
                "Social media feed design",
                "File storage system design"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Gaurav Sen (System Design)",
                "Tech Dummies (Narendra L)",
                "Success in Tech",
                "Engineering with Utsav"
            ],
            "Free Websites": [
                "High Scalability blog",
                "System Design Primer (GitHub - free)",
                "AWS Architecture Center (free articles)",
                "InterviewBit System Design (free tier)"
            ],
            "Free Books/PDFs": [
                "Designing Data-Intensive Applications (some chapters free)",
                "System Design Interview questions (GitHub repos)"
            ]
        }
    },
    "Phase 4: Database Management": {
        "duration": "3-4 weeks",
        "topics": {
            "SQL Fundamentals": [
                "DDL, DML, DCL, TCL commands",
                "Joins: inner, outer, cross, self",
                "Subqueries and correlated queries",
                "Aggregate functions and GROUP BY"
            ],
            "Advanced SQL": [
                "Window functions and ranking",
                "Common Table Expressions (CTEs)",
                "Stored procedures and functions",
                "Triggers and constraints"
            ],
            "Database Design": [
                "ER diagrams and modeling",
                "Normalization (1NF to 3NF)",
                "Primary and foreign keys",
                "Database optimization techniques"
            ],
            "NoSQL Basics": [
                "Document databases (MongoDB)",
                "Key-value stores (Redis)",
                "Column-family (Cassandra)",
                "Graph databases (Neo4j)"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Programming with Mosh (SQL Tutorial)",
                "Derek Banas (Database Tutorial)",
                "Socratica (SQL)",
                "Database Star"
            ],
            "Free Websites": [
                "W3Schools SQL Tutorial",
                "SQLBolt (interactive tutorial)",
                "MySQL Documentation (free)",
                "PostgreSQL Documentation (free)",
                "MongoDB University (free courses)"
            ],
            "Free Books/PDFs": [
                "Learning SQL - free chapters online",
                "Database Systems Concepts (some free versions)",
                "SQLite Documentation (comprehensive and free)"
            ]
        }
    },
    "Phase 5: Web Development": {
        "duration": "5-6 weeks",
        "topics": {
            "Frontend Development": [
                "HTML5: semantic elements, forms, multimedia",
                "CSS3: flexbox, grid, animations, responsive design",
                "JavaScript: DOM manipulation, events, AJAX",
                "Frontend frameworks: React basics or Angular basics"
            ],
            "Backend Development": [
                "Node.js and Express.js fundamentals",
                "RESTful API design and implementation",
                "Authentication and authorization",
                "Server-side templating engines"
            ],
            "Full-Stack Integration": [
                "Frontend-backend communication",
                "API testing with Postman",
                "CORS and security considerations",
                "Deployment basics (Heroku, Netlify)"
            ],
            "Web Technologies": [
                "HTTP/HTTPS protocols",
                "JSON and XML data formats",
                "Web sockets for real-time communication",
                "Progressive Web Apps (PWA) concepts"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Traversy Media (Web Development)",
                "Programming with Mosh (Web Dev)",
                "The Net Ninja",
                "Academind",
                "Dev Ed",
                "Web Dev Simplified"
            ],
            "Free Courses": [
                "freeCodeCamp full-stack curriculum",
                "The Odin Project (completely free)",
                "Mozilla Developer Network (MDN) tutorials",
                "JavaScript.info (free comprehensive guide)"
            ],
            "Free Websites": [
                "W3Schools",
                "CSS-Tricks",
                "MDN Web Docs",
                "Can I Use (browser compatibility)",
                "Flexbox Froggy (CSS Flexbox game)",
                "Grid Garden (CSS Grid game)"
            ]
        }
    },
    "Phase 6: Operating Systems & Computer Networks": {
        "duration": "4-5 weeks",
        "topics": {
            "Operating Systems": [
                "Process management and scheduling",
                "Memory management and virtual memory",
                "File systems and storage management",
                "Synchronization: semaphores, mutexes, deadlocks"
            ],
            "Computer Networks": [
                "OSI and TCP/IP models",
                "HTTP, HTTPS, FTP, DNS protocols",
                "IP addressing and subnetting",
                "Network security basics"
            ],
            "Concurrency": [
                "Threads vs processes",
                "Race conditions and synchronization",
                "Producer-consumer problems",
                "Multi-threading in programming languages"
            ],
            "Linux/Unix Basics": [
                "Command line operations",
                "File permissions and ownership",
                "Shell scripting basics",
                "System monitoring and process management"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Neso Academy (Operating Systems)",
                "Gate Smashers",
                "Knowledge Gate",
                "Ravindrababu Ravula",
                "Computer Science Lessons"
            ],
            "Free Courses": [
                "MIT 6.828 Operating Systems (YouTube)",
                "UC Berkeley CS162 (YouTube)",
                "Coursera Computer Networks (audit free)"
            ],
            "Free Books/PDFs": [
                "Operating System Concepts - free slides/notes",
                "The Linux Command Line (free PDF)",
                "Beej's Guide to Network Programming (free)"
            ],
            "Free Websites": [
                "GeeksforGeeks OS section",
                "Tutorialspoint OS/Networking",
                "Linux man pages online",
                "ExplainShell.com"
            ]
        }
    },
    "Phase 7: Software Engineering Practices": {
        "duration": "3-4 weeks",
        "topics": {
            "Software Development Lifecycle": [
                "Agile and Scrum methodologies",
                "Waterfall model understanding",
                "Requirements gathering and analysis",
                "Software testing phases"
            ],
            "Testing": [
                "Unit testing frameworks (JUnit, pytest)",
                "Integration and system testing",
                "Test-driven development (TDD)",
                "Automated testing concepts"
            ],
            "Design Patterns": [
                "Creational: Singleton, Factory, Builder",
                "Structural: Adapter, Decorator, Facade",
                "Behavioral: Observer, Strategy, Command",
                "MVC architecture pattern"
            ],
            "Code Quality & Maintenance": [
                "Code reviews and best practices",
                "Refactoring techniques",
                "Technical debt management",
                "Documentation standards"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Christopher Okhravi (Design Patterns)",
                "Derek Banas (Design Patterns)",
                "Coding Tech",
                "Continuous Delivery"
            ],
            "Free Books/PDFs": [
                "Design Patterns (free summaries and examples online)",
                "Refactoring Guru (free design patterns guide)",
                "The Pragmatic Programmer (some chapters free online)"
            ],
            "Free Websites": [
                "Refactoring Guru",
                "SourceMaking.com",
                "TutorialsPoint Software Engineering",
                "GeeksforGeeks Software Engineering section"
            ]
        }
    },
    "Phase 8: Advanced Programming Concepts": {
        "duration": "4-5 weeks",
        "topics": {
            "Language-Specific Advanced Topics": [
                "Java: Collections framework, generics, lambda expressions",
                "Python: Decorators, generators, context managers",
                "JavaScript: Closures, prototypes, async/await",
                "C++: Smart pointers, move semantics, templates"
            ],
            "Memory Management": [
                "Stack vs heap memory",
                "Garbage collection concepts",
                "Memory leaks and prevention",
                "Performance optimization"
            ],
            "Advanced Algorithms": [
                "Graph algorithms: Dijkstra, Kruskal, Prim",
                "String algorithms: KMP, Rabin-Karp",
                "Advanced tree structures: B-trees, Red-Black trees",
                "Approximation algorithms"
            ],
            "Competitive Programming": [
                "Fast I/O techniques",
                "Template preparation",
                "Contest strategy and time management",
                "Mathematical programming concepts"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Errichto (Competitive Programming)",
                "CodeChef",
                "William Fiset (Advanced Algorithms)",
                "Tushar Roy"
            ],
            "Free Websites": [
                "Codeforces",
                "AtCoder",
                "SPOJ",
                "CodeChef"
            ],
            "Free Books/PDFs": [
                "Competitive Programming 3 (free chapters)",
                "Advanced Data Structures (online notes)"
            ]
        }
    },
    "Phase 9: Interview Preparation": {
        "duration": "6-8 weeks",
        "topics": {
            "Technical Interview Prep": [
                "Coding interview patterns recognition",
                "Whiteboard coding techniques",
                "Time and space complexity analysis",
                "Problem-solving approach and communication"
            ],
            "System Design Interview": [
                "Scalability principles",
                "Trade-offs discussion",
                "Component interaction diagrams",
                "Capacity estimation techniques"
            ],
            "Behavioral Interview": [
                "STAR method for answering questions",
                "Technical project discussions",
                "Leadership and teamwork examples",
                "Conflict resolution scenarios"
            ],
            "Company-Specific Preparation": [
                "Research target companies",
                "Understanding company culture and values",
                "Recent news and technical blog posts",
                "Glassdoor interview experiences"
            ]
        },
        "resources": {
            "YouTube Channels": [
                "Back To Back SWE (Interview Prep)",
                "Kevin Naughton Jr.",
                "Nick White (LeetCode Solutions)",
                "Clément Mihailescu (AlgoExpert)",
                "Gaurav Sen (System Design Interviews)"
            ],
            "Free Websites": [
                "InterviewBit (free tier)",
                "Pramp (free mock interviews)",
                "GeeksforGeeks interview experiences",
                "LeetCode (free problems)",
                "HackerRank (free challenges)"
            ],
            "Free Books/PDFs": [
                "Cracking the Coding Interview (older editions free)",
                "Interview preparation guides (GitHub repos)",
                "Company-specific interview questions (GitHub)"
            ]
        }
    },
    "Phase 10: Specialization & Career Development": {
        "duration": "Ongoing",
        "topics": {
            "Career Paths": [
                "Software Developer: Frontend, Backend, Full-stack",
                "Data Science: Analytics, Machine Learning, AI",
                "DevOps: Infrastructure, CI/CD, Cloud platforms",
                "Mobile Development: Android, iOS, Cross-platform"
            ],
            "Emerging Technologies": [
                "Cloud Computing: AWS, Azure, Google Cloud",
                "Machine Learning and AI basics",
                "Blockchain and cryptocurrency",
                "Internet of Things (IoT)"
            ],
            "Professional Development": [
                "Open source contributions",
                "Technical blog writing",
                "Conference attendance and networking",
                "Continuous learning mindset"
            ],
            "Certifications": [
                "AWS Certified Developer",
                "Google Cloud Professional",
                "Oracle Certified Java Developer",
                "Microsoft Azure certifications"
            ]
        },
        "resources": {
            "Free Resources": [
                "GitHub for open source contributions",
                "Medium and Dev.to for technical blogging",
                "Meetup.com for local tech events",
                "LinkedIn Learning (free with library card)",
                "YouTube tech conference talks",
                "AWS/Google Cloud free tier accounts",
                "Coursera and edX (audit courses for free)",
                "Stack Overflow for community participation"
            ],
            "YouTube Channels for Trends": [
                "TechLead",
                "Joma Tech",
                "ForrestKnight",
                "Clement Mihailescu",
                "CS Dojo"
            ],
            "Free Learning Platforms": [
                "Kaggle Learn (Data Science)",
                "Google AI Education",
                "Microsoft Learn",
                "freeCodeCamp",
                "Codecademy (free tier)"
            ]
        }
    }
}

# Combined roadmaps
ROADMAPS = {
    "Software Engineer": SOFTWARE_ENGINEER_ROADMAP,
    "ML Research Engineer": ML_RESEARCH_ROADMAP,
    "Quantitative Engineer/Scientist": QUANT_RESEARCH_ROADMAP,
    "CS Fresher": CS_FRESHER_ROADMAP
}


# Key milestones for each track
MILESTONES = {
    "Software Engineer": {
        "Beginner": [
            "Complete first programming project",
            "Solve 50 LeetCode easy problems",
            "Build a personal portfolio website",
            "Contribute to first open-source project"
        ],
        "Intermediate": [
            "Build a full-stack web application",
            "Deploy application to cloud (AWS/GCP/Azure)",
            "Implement CI/CD pipeline",
            "Complete system design of a r# eal-world application"
        ],
        "Advanced": [
            "Lead a technical project",
            "Mentor junior developers",
            "Contribute to major open-source project",
            "Design and implement microservices architecture"
        ]
    },
    "ML Research Engineer": {
        "Computer Vision": [
            "Build a CNN from scratch for image classification",
            "Implement object detection system (YOLO or R-CNN)",
            "Create an image generation model (GAN or Diffusion)",
            "Deploy a real-time CV application"
        ],
        "LLM": [
            "Build a transformer from scratch",
            "Fine-tune a pre-trained model with RLHF",
            "Create a RAG system",
            "Deploy a conversational AI application"
        ],
        "Combined": [
            "Build a vision-language model",
            "Create a multimodal application",
            "Contribute to major open-source projects",
            "Submit research to top-tier conferences"
        ]
    },
        "Quantitative Engineer/Scientist": {
        "Mathematical Foundation": [
            "Implement Black-Scholes pricing from scratch",
            "Build Monte Carlo simulation engine",
            "Create portfolio optimization using mean-variance",
            "Develop basic risk metrics calculator (VaR, Sharpe ratio)"
        ],
        "Trading Systems": [
            "Build a pairs trading strategy with backtesting",
            "Implement momentum strategy with risk management",
            "Create market making algorithm simulation",
            "Develop factor model for stock returns"
        ],
        "Advanced Research": [
            "Build ML-based alpha generation model",
            "Implement systematic risk management framework",
            "Create alternative data integration pipeline",
            "Publish research on novel trading strategy"
        ],
        "Professional": [
            "Pass CFA Level I or FRM Part I certification",
            "Build production trading system",
            "Lead quantitative research project",
            "Present findings at finance conference"
        ]
    },
        "CS Fresher": {
        "Beginner": [
            "Learn basics of programming (Python/Java/C++)",
            "Understand data structures and algorithms (arrays, linked lists)",
            "Solve 50 easy coding problems",
            "Build a basic portfolio project (calculator, to-do app)"
        ],
        "Intermediate": [
            "Learn OOP concepts and implement in a project",
            "Practice 100 DSA problems (LeetCode/Easy + Medium)",
            "Build a small web app using Flask/Django/Node.js",
            "Participate in at least one hackathon"
        ],
        "Advanced": [
            "Understand system design basics (scalability, APIs)",
            "Contribute to open-source project",
            "Build 2-3 production-grade projects (with database + UI)",
            "Prepare for technical interviews (mock practice)"
        ]
    }
}


def save_progress():
    progress_data = {
        "progress": st.session_state.progress,
        "start_date": str(st.session_state.start_date),
        "selected_track": st.session_state.selected_track,
        "last_saved": str(datetime.now())
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress_data, f, indent=2)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            imported_data = json.load(f)
            st.session_state.progress.update(imported_data.get("progress", {}))
            st.session_state.start_date = date.fromisoformat(imported_data.get("start_date", str(date.today())))
            st.session_state.selected_track = imported_data.get("selected_track", list(ROADMAPS.keys())[0])

def calculate_progress():
    """Calculate overall progress percentage"""
    total_items = 0
    completed_items = 0
    
    # Get the currently selected roadmap
    roadmap_data = ROADMAPS[st.session_state.selected_track]
    
    # Count items from roadmap topics
    for phase, phase_data in roadmap_data.items():
        for topic, items in phase_data["topics"].items():
            total_items += len(items)
            for item in items:
                key = f"{phase}|{topic}|{item}"
                if key in st.session_state.progress and st.session_state.progress[key]:
                    completed_items += 1
    
    # Add milestones for the selected track
    milestones_data = MILESTONES[st.session_state.selected_track]
    for category, milestones in milestones_data.items():
        total_items += len(milestones)
        for milestone in milestones:
            key = f"milestone|{category}|{milestone}"
            if key in st.session_state.progress and st.session_state.progress[key]:
                completed_items += 1
    
    return (completed_items / total_items * 100) if total_items > 0 else 0

def main():
    import re  # Added for parsing durations safely

    def parse_duration_to_months(duration):
        """
        Converts a duration string like '6+ months', '3-4 months', '2 months'
        into an integer number of months (approximation).
        """
        numbers = re.findall(r"\d+", duration)
        if not numbers:
            return 0
        if len(numbers) == 2:
            return (int(numbers[0]) + int(numbers[1])) // 2
        return int(numbers[0])

    st.title("🎯 Tech Career Roadmap Tracker")
    
    # Track selection
    track_options = list(ROADMAPS.keys())
    selected_track = st.sidebar.selectbox(
        "Select Career Track",
        track_options,
        index=track_options.index(st.session_state.selected_track) if st.session_state.selected_track in track_options else 0
    )
    st.session_state.selected_track = selected_track
    
    st.markdown(f"Track your progress through the comprehensive {selected_track} learning path.")
    
    # Get the selected roadmap
    ROADMAP_DATA = ROADMAPS[selected_track]
    
    # Sidebar for overall progress
    with st.sidebar:
        st.header("📊 Progress Overview")
        overall_progress = calculate_progress()
        st.metric("Overall Progress", f"{overall_progress:.1f}%")
        st.progress(overall_progress / 100)
        
        # Timeline settings
        st.header("⏱️ Timeline Settings")
        start_date = st.date_input("Start Date", st.session_state.start_date)
        st.session_state.start_date = start_date
        
        # ✅ FIXED: Safe duration parsing
        total_months = sum(parse_duration_to_months(phase_data["duration"]) for phase_data in ROADMAP_DATA.values())
        estimated_completion = start_date + timedelta(days=total_months * 30)
        st.info(f"Estimated Completion: {estimated_completion.strftime('%B %Y')}")
        
        # Export/Import progress
        st.header("💾 Progress Management")
        if st.button("Export Progress"):
            progress_data = {
                "progress": st.session_state.progress,
                "start_date": str(st.session_state.start_date),
                "selected_track": st.session_state.selected_track,
                "export_date": str(datetime.now().date())
            }
            st.download_button(
                "Download Progress JSON",
                json.dumps(progress_data, indent=2),
                file_name=f"{selected_track.replace(' ', '_')}_progress_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            
        uploaded_file = st.file_uploader("Import Progress JSON", type="json")
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                st.session_state.progress.update(imported_data.get("progress", {}))
                if "selected_track" in imported_data:
                    st.session_state.selected_track = imported_data["selected_track"]
                st.success("Progress imported successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error importing progress: {str(e)}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Roadmap", "📈 Analytics", "🏆 Milestones", "📚 Resources"])
    
    with tab1:
        st.header("Learning Roadmap")
        
        for phase_idx, (phase, phase_data) in enumerate(ROADMAP_DATA.items(), 1):
            with st.expander(f"**{phase}** ({phase_data['duration']})", expanded=phase_idx <= 2):
                phase_total = sum(len(items) for items in phase_data["topics"].values())
                phase_completed = 0
                
                for topic, items in phase_data["topics"].items():
                    st.subheader(f"📖 {topic}")
                    topic_completed = 0
                    for item in items:
                        key = f"{phase}|{topic}|{item}"
                        if key not in st.session_state.progress:
                            st.session_state.progress[key] = False
                        
                        is_completed = st.checkbox(item, value=st.session_state.progress[key], key=key)
                        st.session_state.progress[key] = is_completed
                        
                        if is_completed:
                            topic_completed += 1
                            phase_completed += 1
                    
                    if items:
                        topic_progress = (topic_completed / len(items)) * 100
                        st.progress(topic_progress / 100)
                        st.caption(f"Topic Progress: {topic_progress:.0f}% ({topic_completed}/{len(items)})")
                
                if phase_total > 0:
                    phase_progress = (phase_completed / phase_total) * 100
                    st.markdown("---")
                    st.progress(phase_progress / 100)
                    st.info(f"**Phase Progress: {phase_progress:.0f}%** ({phase_completed}/{phase_total} items completed)")
    
    with tab2:
        st.header("Progress Analytics")
        phase_data = []
        for phase, phase_info in ROADMAP_DATA.items():
            phase_total = sum(len(items) for items in phase_info["topics"].values())
            phase_completed = 0
            for topic, items in phase_info["topics"].items():
                for item in items:
                    key = f"{phase}|{topic}|{item}"
                    if key in st.session_state.progress and st.session_state.progress[key]:
                        phase_completed += 1
            if phase_total > 0:
                phase_data.append({
                    "Phase": phase.replace("Phase ", "P"),
                    "Completed": phase_completed,
                    "Total": phase_total,
                    "Progress": (phase_completed / phase_total * 100)
                })
        
        if phase_data:
            df_phases = pd.DataFrame(phase_data)
            fig = px.bar(
                df_phases,
                x="Phase",
                y=["Completed", "Total"],
                title="Progress by Phase",
                color_discrete_map={"Completed": "#00D4AA", "Total": "#E5E5E5"}
            )
            # st.plotly_chart(fig, use_container_width=True)
            st.plotly_chart(fig, width='stretch')
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Topics Completed", sum(df_phases["Completed"]))
            with col2:
                st.metric("Total Topics Remaining", sum(df_phases["Total"]) - sum(df_phases["Completed"]))
            st.subheader("Detailed Progress")
            st.dataframe(df_phases, use_container_width=True)
            # st.dataframe(df_phases, width='stretch')
        else:
            st.info("No progress data available yet.")
    
    with tab3:
        st.header("Key Milestones")
        st.markdown("Track your major achievements and project completions:")
        track_milestones = MILESTONES.get(selected_track, {})
        for category, milestones in track_milestones.items():
            st.subheader(f"🎯 {category}")
            milestone_completed = 0
            for milestone in milestones:
                key = f"milestone|{category}|{milestone}"
                if key not in st.session_state.progress:
                    st.session_state.progress[key] = False
                is_completed = st.checkbox(milestone, value=st.session_state.progress[key], key=key)
                st.session_state.progress[key] = is_completed
                if is_completed:
                    milestone_completed += 1
            if milestones:
                category_progress = (milestone_completed / len(milestones)) * 100
                st.progress(category_progress / 100)
                st.caption(f"{category} Milestones: {milestone_completed}/{len(milestones)} completed")
                st.markdown("---")
    
    with tab4:
        st.header("Essential Resources")
        for phase, phase_data in ROADMAP_DATA.items():
            if "resources" in phase_data:
                st.subheader(f"📚 {phase}")
                for resource_type, resources in phase_data["resources"].items():
                    st.markdown(f"**{resource_type}:**")
                    for resource in resources:
                        st.markdown(f"• {resource}")
                    st.markdown("")

if __name__ == "__main__":
    main() # pyright: ignore[reportShadowedImports]
import streamlit as st
import json
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

PROGRESS_FILE = "progress_data.json"

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
    st.session_state.selected_track = "ML Research Engineer"

# Software Engineer Roadmap
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
            "Courses": [
                "CS50x - Harvard's Introduction to Computer Science (free)",
                "Python for Everybody - University of Michigan (Coursera)",
                "The Odin Project - Foundations (free)"
            ],
            "Books": [
                "Python Crash Course by Eric Matthes",
                "Eloquent JavaScript by Marijn Haverbeke (free online)"
            ],
            "Practice": [
                "Codecademy Interactive Lessons",
                "freeCodeCamp.org"
            ]
        }
    },
    "Phase 2: Data Structures & Algorithms": {
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
                "Union-Find (Disjoint Set)"
            ],
            "Algorithms": [
                "Sorting: Bubble, Selection, Insertion, Merge, Quick, Heap",
                "Searching: Linear, Binary, DFS, BFS",
                "Dynamic Programming",
                "Greedy Algorithms",
                "Backtracking",
                "Graph algorithms: Dijkstra's, Bellman-Ford, Floyd-Warshall"
            ],
            "Complexity Analysis": [
                "Big O notation",
                "Time complexity analysis",
                "Space complexity analysis",
                "Best, average, worst case analysis"
            ]
        },
        "resources": {
            "Courses": [
                "Algorithms Part I & II - Princeton (Coursera)",
                "Data Structures and Algorithms - UC San Diego (Coursera)",
                "MIT 6.006 Introduction to Algorithms (YouTube)"
            ],
            "Books": [
                "Introduction to Algorithms (CLRS)",
                "Algorithm Design Manual by Steven Skiena",
                "Grokking Algorithms by Aditya Bhargava"
            ],
            "Practice": [
                "LeetCode (start with Easy problems)",
                "HackerRank Data Structures track",
                "CodeSignal"
            ]
        }
    },
    "Phase 3: Web Development Fundamentals": {
        "duration": "3-4 months",
        "topics": {
            "Frontend Basics": [
                "HTML5: Semantic markup, forms, accessibility",
                "CSS3: Flexbox, Grid, animations, responsive design",
                "JavaScript: DOM manipulation, events, async programming",
                "Browser DevTools mastery"
            ],
            "Backend Basics": [
                "HTTP/HTTPS protocols",
                "RESTful API design",
                "Server-side programming (Node.js/Python/Java)",
                "Authentication & Authorization",
                "Session management"
            ],
            "Databases": [
                "SQL fundamentals: CRUD, Joins, Indexes",
                "Relational databases: PostgreSQL, MySQL",
                "NoSQL basics: MongoDB, Redis",
                "Database design and normalization",
                "ORMs and Query builders"
            ],
            "Version Control": [
                "Git fundamentals",
                "Branching strategies (Git Flow, GitHub Flow)",
                "Pull requests and code reviews",
                "Resolving merge conflicts"
            ]
        },
        "resources": {
            "Courses": [
                "The Odin Project - Full Stack JavaScript (free)",
                "Full Stack Open - University of Helsinki (free)",
                "CS50's Web Programming with Python and JavaScript"
            ],
            "Books": [
                "MDN Web Docs (comprehensive web reference)",
                "You Don't Know JS series by Kyle Simpson",
                "SQL in 10 Minutes by Ben Forta"
            ],
            "Practice": [
                "Frontend Mentor (real projects)",
                "Build personal portfolio website",
                "Contribute to open source projects"
            ]
        }
    },
    "Phase 4: Modern Frameworks & Tools": {
        "duration": "3-4 months",
        "topics": {
            "Frontend Frameworks": [
                "React.js: Components, hooks, state management",
                "Vue.js or Angular basics",
                "State management: Redux, Context API, Zustand",
                "Next.js/Nuxt.js for SSR/SSG",
                "CSS frameworks: Tailwind, Material-UI"
            ],
            "Backend Frameworks": [
                "Express.js/Fastify (Node.js)",
                "Django/FastAPI (Python)",
                "Spring Boot (Java)",
                "GraphQL basics",
                "Microservices architecture"
            ],
            "Development Tools": [
                "Package managers: npm, yarn, pip",
                "Build tools: Webpack, Vite, Rollup",
                "Testing: Jest, Pytest, Cypress",
                "CI/CD pipelines",
                "Docker containerization"
            ],
            "Cloud Platforms": [
                "AWS basics: EC2, S3, Lambda",
                "Google Cloud Platform or Azure",
                "Serverless architecture",
                "CDN and caching strategies"
            ]
        },
        "resources": {
            "Courses": [
                "React - The Complete Guide (Udemy - Maximilian Schwarzmüller)",
                "Node.js, Express, MongoDB Bootcamp (Udemy - Jonas Schmedtmann)",
                "Docker and Kubernetes: The Complete Guide (Udemy)"
            ],
            "Books": [
                "Learning React by Alex Banks & Eve Porcello",
                "Node.js Design Patterns by Mario Casciaro",
                "Clean Code by Robert C. Martin"
            ],
            "Practice": [
                "Build a full-stack CRUD application",
                "Create a real-time chat application",
                "Deploy projects to cloud platforms"
            ]
        }
    },
    "Phase 5: Software Engineering Practices": {
        "duration": "2-3 months",
        "topics": {
            "Design Patterns": [
                "Creational: Singleton, Factory, Builder",
                "Structural: Adapter, Decorator, Facade",
                "Behavioral: Observer, Strategy, Command",
                "MVC, MVP, MVVM architectures",
                "SOLID principles"
            ],
            "Testing": [
                "Unit testing",
                "Integration testing",
                "End-to-end testing",
                "Test-Driven Development (TDD)",
                "Behavior-Driven Development (BDD)"
            ],
            "Code Quality": [
                "Clean code principles",
                "Code reviews best practices",
                "Refactoring techniques",
                "Documentation",
                "Linting and formatting"
            ],
            "Agile & Project Management": [
                "Scrum methodology",
                "Kanban boards",
                "Sprint planning and retrospectives",
                "User stories and estimation",
                "JIRA/Linear/Trello"
            ]
        },
        "resources": {
            "Courses": [
                "Software Design and Architecture (Coursera)",
                "Test-Driven Development with Python (O'Reilly)",
                "Agile Development Specialization (Coursera)"
            ],
            "Books": [
                "Design Patterns: Elements of Reusable Object-Oriented Software",
                "Refactoring by Martin Fowler",
                "The Pragmatic Programmer by David Thomas & Andrew Hunt"
            ],
            "Practice": [
                "Refactor existing code using design patterns",
                "Write comprehensive test suites",
                "Participate in code reviews"
            ]
        }
    },
    "Phase 6: System Design & Architecture": {
        "duration": "3-4 months",
        "topics": {
            "System Design Fundamentals": [
                "Scalability: Horizontal vs Vertical",
                "Load balancing strategies",
                "Caching: Browser, CDN, Application, Database",
                "Database sharding and replication",
                "CAP theorem"
            ],
            "Distributed Systems": [
                "Microservices vs Monolithic",
                "Service discovery",
                "Message queues: RabbitMQ, Kafka",
                "API Gateway patterns",
                "Event-driven architecture"
            ],
            "Performance & Optimization": [
                "Performance profiling",
                "Database query optimization",
                "Caching strategies",
                "Lazy loading and code splitting",
                "CDN optimization"
            ],
            "Security": [
                "OWASP Top 10",
                "Authentication: JWT, OAuth 2.0",
                "Encryption and hashing",
                "SQL injection prevention",
                "XSS and CSRF protection"
            ]
        },
        "resources": {
            "Courses": [
                "Grokking the System Design Interview (Educative)",
                "System Design Interview Course (Alex Xu)",
                "Distributed Systems - MIT 6.824"
            ],
            "Books": [
                "Designing Data-Intensive Applications by Martin Kleppmann",
                "System Design Interview by Alex Xu",
                "Building Microservices by Sam Newman"
            ],
            "Practice": [
                "Design Twitter/Instagram clone",
                "Design URL shortener",
                "Design distributed cache"
            ]
        }
    },
    "Phase 7: Advanced Backend Development": {
        "duration": "3-4 months",
        "topics": {
            "Advanced Database Concepts": [
                "Transaction isolation levels",
                "Database indexing strategies",
                "Query optimization",
                "Database migrations",
                "Time-series databases"
            ],
            "API Development": [
                "RESTful API best practices",
                "GraphQL implementation",
                "gRPC and Protocol Buffers",
                "API versioning",
                "Rate limiting and throttling"
            ],
            "Real-time Systems": [
                "WebSockets implementation",
                "Server-Sent Events (SSE)",
                "Long polling",
                "Real-time databases (Firebase, Supabase)",
                "Push notifications"
            ],
            "Search & Analytics": [
                "Elasticsearch implementation",
                "Full-text search",
                "Analytics pipelines",
                "Log aggregation",
                "Monitoring and alerting"
            ]
        },
        "resources": {
            "Courses": [
                "Advanced Node.js (Frontend Masters)",
                "Database Engineering (Hussein Nasser - Udemy)",
                "Real-time Web with Node.js (Pluralsight)"
            ],
            "Books": [
                "High Performance Browser Networking by Ilya Grigorik",
                "Database Internals by Alex Petrov",
                "Elasticsearch: The Definitive Guide"
            ],
            "Practice": [
                "Build a real-time collaboration tool",
                "Implement search functionality",
                "Create analytics dashboard"
            ]
        }
    },
    "Phase 8: DevOps & Infrastructure": {
        "duration": "3-4 months",
        "topics": {
            "Containerization & Orchestration": [
                "Docker deep dive",
                "Kubernetes fundamentals",
                "Helm charts",
                "Service mesh (Istio)",
                "Container security"
            ],
            "CI/CD Pipelines": [
                "Jenkins/GitHub Actions/GitLab CI",
                "Automated testing in CI/CD",
                "Blue-green deployments",
                "Canary releases",
                "Infrastructure as Code"
            ],
            "Monitoring & Logging": [
                "Prometheus and Grafana",
                "ELK Stack (Elasticsearch, Logstash, Kibana)",
                "APM tools (New Relic, DataDog)",
                "Distributed tracing",
                "Error tracking (Sentry)"
            ],
            "Cloud Native": [
                "Serverless architectures",
                "Function as a Service (FaaS)",
                "API Gateway",
                "Cloud databases",
                "Auto-scaling strategies"
            ]
        },
        "resources": {
            "Courses": [
                "Docker and Kubernetes: The Complete Guide (Udemy)",
                "DevOps Bootcamp (Techworld with Nana)",
                "AWS Certified Solutions Architect (A Cloud Guru)"
            ],
            "Books": [
                "The DevOps Handbook",
                "Kubernetes in Action by Marko Lukša",
                "Site Reliability Engineering (Google)"
            ],
            "Practice": [
                "Set up complete CI/CD pipeline",
                "Deploy application to Kubernetes",
                "Implement monitoring and alerting"
            ]
        }
    },
    "Phase 9: Specialization Tracks": {
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
            ]
        },
        "resources": {
            "Courses": [
                "Epic React by Kent C. Dodds",
                "Distributed Systems & Cloud Computing (Stanford)",
                "Practical Security for Developers (Auth0)"
            ],
            "Books": [
                "Staff Engineer by Will Larson",
                "The Phoenix Project",
                "Accelerate by Nicole Forsgren"
            ],
            "Practice": [
                "Contribute to major open-source projects",
                "Build production-ready applications",
                "Write technical blog posts"
            ]
        }
    },
    "Phase 10: Senior Engineering Skills": {
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
            "Courses": [
                "Engineering Management (Coursera)",
                "Technical Writing (Google)",
                "Leadership Principles (LinkedIn Learning)"
            ],
            "Books": [
                "The Manager's Path by Camille Fournier",
                "An Elegant Puzzle by Will Larson",
                "The Effective Engineer by Edmond Lau"
            ],
            "Practice": [
                "Lead technical projects",
                "Mentor team members",
                "Speak at meetups/conferences"
            ]
        }
    }
}

# ML Research Engineer Roadmap (existing)
ML_RESEARCH_ROADMAP = {
    "Phase 1: Mathematical Foundations": {
        "duration": "3-4 months",
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
                "Deep Learning - Ian Goodfellow"
            ]
        }
    },
    "Phase 2: Programming & Tools": {
        "duration": "2-3 months",
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
                "Cloud platforms with GPU support"
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
        "topics": {
            "Traditional ML Concepts": [
                "Linear/logistic regression",
                "Decision trees, random forests",
                "Support vector machines",
                "Neural networks fundamentals"
            ],
            "Data Processing": [
                "For CV: Image preprocessing, augmentation techniques",
                "For LLM: Text preprocessing, tokenization basics",
                "Feature engineering principles"
            ],
            "Model Evaluation & Selection": [
                "Cross-validation",
                "Bias-variance tradeoff",
                "Regularization techniques",
                "CV metrics: Accuracy, IoU, mAP",
                "LLM metrics: BLEU, ROUGE, perplexity"
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
        "topics": {
            "Neural Network Fundamentals": [
                "Backpropagation algorithm",
                "Activation functions, loss functions",
                "Gradient descent variants"
            ],
            "Core Architectures": [
                "Feedforward networks",
                "Convolutional Neural Networks (CNNs) - essential for CV",
                "Recurrent Neural Networks (RNNs, LSTMs, GRUs) - foundation for LLMs"
            ],
            "Advanced Topics": [
                "Transfer learning",
                "Regularization techniques",
                "Advanced optimizers"
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
    "Phase 5: Foundation Specialization": {
        "duration": "3-4 months",
        "topics": {
            "Option A: Computer Vision Foundation": [
                "Image fundamentals: pixels, channels, color spaces",
                "Basic operations: filtering, edge detection, morphological operations",
                "Feature extraction: SIFT, SURF, HOG",
                "Classical techniques: template matching, contour detection"
            ],
            "Option B: NLP Foundation": [
                "Classical NLP: n-grams, POS tagging, NER",
                "Word embeddings: Word2Vec, GloVe, FastText",
                "Sequence models: basic RNNs for text",
                "Text preprocessing: tokenization, normalization"
            ]
        },
        "resources": {
            "Courses": [
                "CS231n - Stanford Computer Vision",
                "CS224N - Stanford NLP with Deep Learning"
            ],
            "Books": [
                "Computer Vision: Algorithms and Applications",
                "Speech and Language Processing - Jurafsky & Martin"
            ]
        }
    },
    "Phase 6: Advanced Deep Learning Architectures": {
        "duration": "4-6 months",
        "topics": {
            "Computer Vision Track - CNN Architectures": [
                "LeNet, AlexNet, VGG, ResNet",
                "Inception, DenseNet, EfficientNet",
                "Vision Transformers (ViTs)"
            ],
            "Computer Vision Track - Specialized CV Tasks": [
                "Image Classification: Multi-class, multi-label",
                "Object Detection: R-CNN family, YOLO, SSD",
                "Semantic Segmentation: U-Net, DeepLab, Mask R-CNN",
                "Instance Segmentation: Mask R-CNN, SOLO"
            ],
            "LLM Track - Transformer Architecture": [
                "Attention mechanisms deep dive",
                "Encoder-decoder structure",
                "Implementation from scratch"
            ],
            "LLM Track - Large Language Models": [
                "GPT series evolution",
                "BERT and bidirectional models",
                "T5, PaLM, modern architectures"
            ]
        },
        "resources": {
            "Courses": [
                "Transformers Course - HuggingFace",
                "Advanced Computer Vision - Coursera"
            ],
            "Papers": [
                "Attention Is All You Need",
                "BERT, GPT papers series"
            ]
        }
    },
    "Phase 7: Specialization Deep Dive": {
        "duration": "4-6 months each",
        "topics": {
            "CV - Medical Imaging": [
                "X-ray analysis, MRI/CT scan interpretation, pathology",
                "3D CNNs, attention mechanisms for medical data",
                "Tools: SimpleITK, MONAI, PyDicom"
            ],
            "CV - Autonomous Vehicles": [
                "Object detection, lane detection, depth estimation",
                "Real-time processing, sensor fusion, 3D object detection",
                "Tools: CARLA simulator, ROS, Point Cloud Library"
            ],
            "LLM - Conversational AI": [
                "Chatbots, virtual assistants, dialogue systems",
                "Multi-turn conversations, context management",
                "Tools: Rasa, DialoGPT, ChatGPT API"
            ],
            "LLM - Code Generation": [
                "GitHub Copilot-style systems, code explanation",
                "Code understanding, syntax-aware generation",
                "Tools: CodeT5, InCoder, StarCoder"
            ]
        },
        "resources": {
            "Specialized Courses": [
                "Medical Image Analysis - Coursera",
                "Self-Driving Cars Specialization - Coursera"
            ],
            "Domain Papers": [
                "Recent conference papers from CVPR, NeurIPS, ACL"
            ]
        }
    },
    "Phase 8: Advanced Research Techniques": {
        "duration": "4-5 months",
        "topics": {
            "For Computer Vision": [
                "Self-supervised learning: Contrastive learning, masked image modeling",
                "Few-shot learning: Prototypical networks, meta-learning",
                "Domain adaptation: Transfer between different visual domains",
                "Interpretability: Grad-CAM, attention visualization, saliency maps"
            ],
            "For LLMs": [
                "Training optimizations: Distributed training, memory optimization",
                "Inference optimization: Model compression, efficient serving",
                "Safety and alignment: Constitutional AI, bias mitigation",
                "Tool use: Function calling, API integration"
            ],
            "Common Advanced Topics": [
                "Neural Architecture Search (NAS)",
                "Federated learning",
                "Continual learning",
                "Robustness and adversarial training"
            ]
        },
        "resources": {
            "Advanced Courses": [
                "Advanced Deep Learning - MIT",
                "Research Methods in ML - Stanford"
            ],
            "Cutting-edge Papers": [
                "Latest papers from arXiv",
                "Conference proceedings"
            ]
        }
    },
    "Phase 9: Research Skills & Paper Implementation": {
        "duration": "4-6 months",
        "topics": {
            "CV Paper Reading": [
                "Foundational: LeNet, AlexNet, ResNet, 'Attention Is All You Need'",
                "Recent: Vision Transformers, CLIP, DALL-E 2, Stable Diffusion",
                "Venues: CVPR, ICCV, ECCV, NeurIPS, ICLR"
            ],
            "LLM Paper Reading": [
                "Foundational: Transformer, GPT series, BERT, T5",
                "Recent: InstructGPT, ChatGPT, GPT-4, Constitutional AI",
                "Venues: ACL, EMNLP, ICLR, NeurIPS, ICML"
            ],
            "Implementation Projects": [
                "Reproduce 2-3 CV papers from scratch",
                "Reproduce 2-3 LLM papers from scratch",
                "Create novel combinations of existing techniques",
                "Build end-to-end applications"
            ]
        },
        "resources": {
            "Paper Resources": [
                "Papers with Code",
                "arXiv.org",
                "Conference websites"
            ],
            "Implementation Guides": [
                "Annotated implementations",
                "YouTube paper walkthroughs"
            ]
        }
    },
    "Phase 10: Original Research & Specialization": {
        "duration": "6+ months",
        "topics": {
            "Research Areas at the Intersection": [
                "Vision-Language Models: The future of AI",
                "Multimodal reasoning: Combining visual and textual understanding",
                "Embodied AI: Connecting vision, language, and robotics",
                "Scientific applications: Using both CV and LLM for research"
            ],
            "Build Research Portfolio": [
                "GitHub with high-quality implementations",
                "Technical blog posts",
                "Open-source contributions",
                "Conference submissions",
                "Collaboration with research groups"
            ]
        },
        "resources": {
            "Research Communities": [
                "ML Twitter/X community",
                "Research group collaborations",
                "Conference attendance"
            ],
            "Publishing Venues": [
                "Top-tier conferences",
                "Workshops",
                "arXiv preprints"
            ]
        }
    }
}

# Combined roadmaps
ROADMAPS = {
    "Software Engineer": SOFTWARE_ENGINEER_ROADMAP,
    "ML Research Engineer": ML_RESEARCH_ROADMAP
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
            "Complete system design of a real-world application"
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
    }
}

# def save_progress():
#     """Save progress to session state"""
#     pass  # Progress is automatically saved in session state

# def load_progress():
#     """Load progress from session state"""
#     return st.session_state.progress

# def calculate_progress():
#     """Calculate overall progress percentage"""
#     total_items = 0
#     completed_items = 0
    
#     for phase, phase_data in ROADMAP_DATA.items():
#         for topic, items in phase_data["topics"].items():
#             total_items += len(items)
#             for item in items:
#                 key = f"{phase}|{topic}|{item}"
#                 if key in st.session_state.progress and st.session_state.progress[key]:
#                     completed_items += 1
    
#     # Add milestones
#     for category, milestones in MILESTONES.items():
#         total_items += len(milestones)
#         for milestone in milestones:
#             key = f"milestone|{category}|{milestone}"
#             if key in st.session_state.progress and st.session_state.progress[key]:
#                 completed_items += 1
    
#     return (completed_items / total_items * 100) if total_items > 0 else 0

# def main():
#     st.title("🎯 ML Research Engineer Roadmap Tracker")
#     st.markdown("Track your progress through the comprehensive ML Research Engineer learning path covering both Computer Vision and LLM specializations.")
    
#     # Sidebar for overall progress
#     with st.sidebar:
#         st.header("📊 Progress Overview")
#         overall_progress = calculate_progress()
#         st.metric("Overall Progress", f"{overall_progress:.1f}%")
#         st.progress(overall_progress / 100)
        
#         # Timeline settings
#         st.header("⏱️ Timeline Settings")
#         start_date = st.date_input("Start Date", st.session_state.start_date)
#         st.session_state.start_date = start_date
        
#         estimated_completion = start_date + timedelta(days=44*30)  # 44 months
#         st.info(f"Estimated Completion: {estimated_completion.strftime('%B %Y')}")
        
#         # Export/Import progress
#         st.header("💾 Progress Management")
#         if st.button("Export Progress"):
#             progress_data = {
#                 "progress": st.session_state.progress,
#                 "start_date": str(st.session_state.start_date),
#                 "export_date": str(datetime.now().date())
#             }
#             st.download_button(
#                 "Download Progress JSON",
#                 json.dumps(progress_data, indent=2),
#                 file_name=f"ml_roadmap_progress_{datetime.now().strftime('%Y%m%d')}.json",
#                 mime="application/json"
#             )
    
#     # Main content tabs
#     tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Roadmap", "📈 Analytics", "🏆 Milestones", "📚 Resources"])
    
#     with tab1:
#         st.header("Learning Roadmap")
        
#         # Phase progress
#         for phase_idx, (phase, phase_data) in enumerate(ROADMAP_DATA.items(), 1):
#             with st.expander(f"**{phase}** ({phase_data['duration']})", expanded=phase_idx <= 2):
                
#                 # Calculate phase progress
#                 phase_total = sum(len(items) for items in phase_data["topics"].values())
#                 phase_completed = 0
                
#                 for topic, items in phase_data["topics"].items():
#                     st.subheader(f"📖 {topic}")
                    
#                     # Topic progress
#                     topic_completed = 0
#                     for item in items:
#                         key = f"{phase}|{topic}|{item}"
#                         if key not in st.session_state.progress:
#                             st.session_state.progress[key] = False
                        
#                         is_completed = st.checkbox(
#                             item,
#                             value=st.session_state.progress[key],
#                             key=key
#                         )
#                         st.session_state.progress[key] = is_completed
                        
#                         if is_completed:
#                             topic_completed += 1
#                             phase_completed += 1
                    
#                     # Topic progress bar
#                     topic_progress = (topic_completed / len(items)) * 100 if items else 0
#                     st.progress(topic_progress / 100)
#                     st.caption(f"Topic Progress: {topic_progress:.0f}% ({topic_completed}/{len(items)})")
                
#                 # Phase progress bar
#                 phase_progress = (phase_completed / phase_total) * 100 if phase_total else 0
#                 st.markdown("---")
#                 st.progress(phase_progress / 100)
#                 st.info(f"**Phase Progress: {phase_progress:.0f}%** ({phase_completed}/{phase_total} items completed)")
    
#     with tab2:
#         st.header("Progress Analytics")
        
#         # Progress by phase
#         phase_data = []
#         for phase, phase_info in ROADMAP_DATA.items():
#             phase_total = sum(len(items) for items in phase_info["topics"].values())
#             phase_completed = 0
            
#             for topic, items in phase_info["topics"].items():
#                 for item in items:
#                     key = f"{phase}|{topic}|{item}"
#                     if key in st.session_state.progress and st.session_state.progress[key]:
#                         phase_completed += 1
            
#             phase_data.append({
#                 "Phase": phase.replace("Phase ", "P"),
#                 "Completed": phase_completed,
#                 "Total": phase_total,
#                 "Progress": (phase_completed / phase_total * 100) if phase_total else 0
#             })
        
#         df_phases = pd.DataFrame(phase_data)
        
#         # Progress chart
#         fig = px.bar(
#             df_phases,
#             x="Phase",
#             y=["Completed", "Total"],
#             title="Progress by Phase",
#             color_discrete_map={"Completed": "#00D4AA", "Total": "#E5E5E5"}
#         )
#         st.plotly_chart(fig, use_container_width=True)
        
#         # Progress timeline
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Total Topics Completed", sum(df_phases["Completed"]))
#         with col2:
#             st.metric("Total Topics Remaining", sum(df_phases["Total"]) - sum(df_phases["Completed"]))
        
#         # Detailed progress table
#         st.subheader("Detailed Progress")
#         st.dataframe(df_phases, use_container_width=True)
    
#     with tab3:
#         st.header("Key Milestones")
#         st.markdown("Track your major achievements and project completions:")
        
#         for category, milestones in MILESTONES.items():
#             st.subheader(f"🎯 {category}")
            
#             milestone_completed = 0
#             for milestone in milestones:
#                 key = f"milestone|{category}|{milestone}"
#                 if key not in st.session_state.progress:
#                     st.session_state.progress[key] = False
                
#                 is_completed = st.checkbox(
#                     milestone,
#                     value=st.session_state.progress[key],
#                     key=key
#                 )
#                 st.session_state.progress[key] = is_completed
                
#                 if is_completed:
#                     milestone_completed += 1
            
#             # Category progress
#             category_progress = (milestone_completed / len(milestones)) * 100
#             st.progress(category_progress / 100)
#             st.caption(f"{category} Milestones: {milestone_completed}/{len(milestones)} completed")
#             st.markdown("---")
    
#     with tab4:
#         st.header("Essential Resources")
        
#         resources = {
#             "📚 Books": [
#                 "Hands-On Machine Learning by Aurélien Géron",
#                 "Deep Learning by Ian Goodfellow",
#                 "Natural Language Processing with Transformers",
#                 "Speech and Language Processing by Jurafsky & Martin"
#             ],
#             "🎓 Courses": [
#                 "Andrew Ng's Machine Learning Course",
#                 "Deep Learning Specialization (Coursera)",
#                 "CS224N Stanford NLP Course",
#                 "HuggingFace Course"
#             ],
#             "📄 Key Papers": [
#                 "'Attention Is All You Need' (Transformer)",
#                 "GPT, GPT-2, GPT-3 paper series",
#                 "BERT, RoBERTa, T5 papers",
#                 "ResNet, Vision Transformer papers"
#             ],
#             "🛠️ Tools & Libraries": [
#                 "PyTorch, TensorFlow",
#                 "HuggingFace Transformers",
#                 "OpenCV, PIL/Pillow",
#                 "Weights & Biases, MLflow"
#             ],
#             "🌐 Communities": [
#                 "r/MachineLearning",
#                 "HuggingFace Forums",
#                 "Papers With Code",
#                 "ML Twitter Community"
#             ]
#         }
        
#         for category, items in resources.items():
#             st.subheader(category)
#             for item in items:
#                 st.markdown(f"• {item}")
#             st.markdown("")


# def save_progress():
#     """Save progress to session state"""
#     # Progress is automatically saved in session state through checkbox interactions
#     # No additional action needed as Streamlit maintains session state
#     pass

# def load_progress():
#     """Load progress from session state"""
#     return st.session_state.get('progress', {})

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
            st.plotly_chart(fig, use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Topics Completed", sum(df_phases["Completed"]))
            with col2:
                st.metric("Total Topics Remaining", sum(df_phases["Total"]) - sum(df_phases["Completed"]))
            st.subheader("Detailed Progress")
            st.dataframe(df_phases, use_container_width=True)
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
    main()
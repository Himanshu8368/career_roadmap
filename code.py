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
    st.session_state.selected_track = "ML Research Engineer"


# 1. ADD THIS TO SESSION STATE INITIALIZATION (after existing session state)
if 'notes' not in st.session_state:
    st.session_state.notes = {}

PROGRESS_FILE = "progress_data.json"


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
# ML_RESEARCH_ROADMAP = {

#     "Phase 1: Mathematical Foundations": {
#         "duration": "3-4 months",
#         "topics": {
#             "Linear Algebra": [
#                 "Vectors, matrices, eigenvalues, eigenvectors",
#                 "Matrix decompositions (SVD, PCA)",
#                 "LLM-specific: Understanding attention as matrix operations",
#                 "CV-specific: Understanding convolutions as matrix operations"
#             ],
#             "Calculus & Optimization": [
#                 "Derivatives, partial derivatives, chain rule",
#                 "Gradients, Hessians",
#                 "Convex optimization basics",
#                 "LLM-specific: Understanding gradient flow in transformer training",
#                 "CV-specific: Understanding backpropagation in CNNs"
#             ],
#             "Statistics & Probability": [
#                 "Probability distributions, Bayes' theorem",
#                 "Hypothesis testing, confidence intervals",
#                 "Maximum likelihood estimation",
#                 "LLM-specific: Language modeling as probability estimation",
#                 "CV-specific: Understanding uncertainty in vision tasks"
#             ],
#             "Information Theory": [
#                 "Entropy, mutual information",
#                 "Cross-entropy loss intuition"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "Mathematics for Machine Learning (Coursera)",
#                 "Linear Algebra - MIT OCW",
#                 "Statistical Learning - Stanford"
#             ],
#             "Books": [
#                 "Pattern Recognition and Machine Learning - Bishop",
#                 "The Elements of Statistical Learning",
#                 "Deep Learning - Ian Goodfellow"
#             ]
#         }
#     },
#     "Phase 2: Programming & Tools": {
#         "duration": "2-3 months",
#         "topics": {
#             "Python Mastery": [
#                 "Data structures, OOP, functional programming",
#                 "NumPy, Pandas, Matplotlib, Seaborn",
#                 "Jupyter notebooks, debugging"
#             ],
#             "Machine Learning Libraries": [
#                 "Scikit-learn for traditional ML",
#                 "PyTorch (preferred for both LLM and CV research)",
#                 "CV libraries: OpenCV, PIL/Pillow, scikit-image",
#                 "LLM libraries: HuggingFace Transformers, tokenizers"
#             ],
#             "Specialized Tools": [
#                 "For CV: Albumentations, YOLO, detectron2",
#                 "For LLM: HuggingFace ecosystem, DeepSpeed, vLLM",
#                 "Common: Weights & Biases for experiment tracking"
#             ],
#             "Development Tools": [
#                 "Git/GitHub for version control",
#                 "Command line proficiency",
#                 "Docker basics",
#                 "Cloud platforms with GPU support"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "Python for Data Science - Coursera",
#                 "PyTorch Fundamentals - PyTorch.org",
#                 "Practical Deep Learning - fast.ai"
#             ],
#             "Books": [
#                 "Hands-On Machine Learning - Aurélien Géron",
#                 "Programming PyTorch for Deep Learning"
#             ]
#         }
#     },
#     "Phase 3: Core Machine Learning": {
#         "duration": "4-5 months",
#         "topics": {
#             "Traditional ML Concepts": [
#                 "Linear/logistic regression",
#                 "Decision trees, random forests",
#                 "Support vector machines",
#                 "Neural networks fundamentals"
#             ],
#             "Data Processing": [
#                 "For CV: Image preprocessing, augmentation techniques",
#                 "For LLM: Text preprocessing, tokenization basics",
#                 "Feature engineering principles"
#             ],
#             "Model Evaluation & Selection": [
#                 "Cross-validation",
#                 "Bias-variance tradeoff",
#                 "Regularization techniques",
#                 "CV metrics: Accuracy, IoU, mAP",
#                 "LLM metrics: BLEU, ROUGE, perplexity"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "Machine Learning - Andrew Ng (Coursera)",
#                 "CS229 - Stanford Machine Learning"
#             ],
#             "Books": [
#                 "An Introduction to Statistical Learning",
#                 "Machine Learning Yearning - Andrew Ng"
#             ]
#         }
#     },
#     "Phase 4: Deep Learning Fundamentals": {
#         "duration": "3-4 months",
#         "topics": {
#             "Neural Network Fundamentals": [
#                 "Backpropagation algorithm",
#                 "Activation functions, loss functions",
#                 "Gradient descent variants"
#             ],
#             "Core Architectures": [
#                 "Feedforward networks",
#                 "Convolutional Neural Networks (CNNs) - essential for CV",
#                 "Recurrent Neural Networks (RNNs, LSTMs, GRUs) - foundation for LLMs"
#             ],
#             "Advanced Topics": [
#                 "Transfer learning",
#                 "Regularization techniques",
#                 "Advanced optimizers"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "Deep Learning Specialization - Andrew Ng",
#                 "CS231n - Stanford CNN for Visual Recognition"
#             ],
#             "Books": [
#                 "Deep Learning - Goodfellow, Bengio, Courville"
#             ]
#         }
#     },
#     "Phase 5: Foundation Specialization": {
#         "duration": "3-4 months",
#         "topics": {
#             "Option A: Computer Vision Foundation": [
#                 "Image fundamentals: pixels, channels, color spaces",
#                 "Basic operations: filtering, edge detection, morphological operations",
#                 "Feature extraction: SIFT, SURF, HOG",
#                 "Classical techniques: template matching, contour detection"
#             ],
#             "Option B: NLP Foundation": [
#                 "Classical NLP: n-grams, POS tagging, NER",
#                 "Word embeddings: Word2Vec, GloVe, FastText",
#                 "Sequence models: basic RNNs for text",
#                 "Text preprocessing: tokenization, normalization"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "CS231n - Stanford Computer Vision",
#                 "CS224N - Stanford NLP with Deep Learning"
#             ],
#             "Books": [
#                 "Computer Vision: Algorithms and Applications",
#                 "Speech and Language Processing - Jurafsky & Martin"
#             ]
#         }
#     },
#     "Phase 6: Advanced Deep Learning Architectures": {
#         "duration": "4-6 months",
#         "topics": {
#             "Computer Vision Track - CNN Architectures": [
#                 "LeNet, AlexNet, VGG, ResNet",
#                 "Inception, DenseNet, EfficientNet",
#                 "Vision Transformers (ViTs)"
#             ],
#             "Computer Vision Track - Specialized CV Tasks": [
#                 "Image Classification: Multi-class, multi-label",
#                 "Object Detection: R-CNN family, YOLO, SSD",
#                 "Semantic Segmentation: U-Net, DeepLab, Mask R-CNN",
#                 "Instance Segmentation: Mask R-CNN, SOLO"
#             ],
#             "LLM Track - Transformer Architecture": [
#                 "Attention mechanisms deep dive",
#                 "Encoder-decoder structure",
#                 "Implementation from scratch"
#             ],
#             "LLM Track - Large Language Models": [
#                 "GPT series evolution",
#                 "BERT and bidirectional models",
#                 "T5, PaLM, modern architectures"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "Transformers Course - HuggingFace",
#                 "Advanced Computer Vision - Coursera"
#             ],
#             "Papers": [
#                 "Attention Is All You Need",
#                 "BERT, GPT papers series"
#             ]
#         }
#     },
#     "Phase 6.5: Reinforcement Learning Fundamentals": {
#         "duration": "3-4 months",
#         "topics": {
#             "Core RL Concepts": [
#                 "Markov Decision Processes (MDPs)",
#                 "Value functions, policy functions",
#                 "Bellman equations and dynamic programming",
#                 "Exploration vs exploitation trade-off"
#             ],
#             "Classical RL Algorithms": [
#                 "Q-Learning, SARSA",
#                 "Policy gradient methods",
#                 "Temporal difference learning",
#                 "Monte Carlo methods"
#             ],
#             "Deep Reinforcement Learning": [
#                 "Deep Q-Networks (DQN) and variants",
#                 "Actor-Critic methods (A2C, A3C)",
#                 "Proximal Policy Optimization (PPO)",
#                 "Deep Deterministic Policy Gradient (DDPG)"
#             ],
#             "Advanced RL Topics": [
#                 "Multi-agent reinforcement learning",
#                 "Hierarchical reinforcement learning",
#                 "Inverse reinforcement learning",
#                 "RLHF (Reinforcement Learning from Human Feedback)"
#             ]
#         },
#         "resources": {
#             "Courses": [
#                 "CS285 - UC Berkeley Deep RL",
#                 "Reinforcement Learning Specialization - University of Alberta",
#                 "DeepMind RL Course"
#             ],
#             "Books": [
#                 "Reinforcement Learning: An Introduction - Sutton & Barto",
#                 "Deep Reinforcement Learning Hands-On - Maxim Lapan"
#             ],
#             "Libraries": [
#                 "OpenAI Gym, Gymnasium",
#                 "Stable Baselines3",
#                 "Ray RLlib",
#                 "TensorFlow Agents"
#             ]
#         }
#     },
#     "Phase 7: Specialization Deep Dive": {
#         "duration": "4-6 months each",
#         "topics": {
#             "CV - Medical Imaging": [
#                 "X-ray analysis, MRI/CT scan interpretation, pathology",
#                 "3D CNNs, attention mechanisms for medical data",
#                 "Tools: SimpleITK, MONAI, PyDicom"
#             ],
#             "CV - Autonomous Vehicles": [
#                 "Object detection, lane detection, depth estimation",
#                 "Real-time processing, sensor fusion, 3D object detection",
#                 "Tools: CARLA simulator, ROS, Point Cloud Library"
#             ],
#             "LLM - Conversational AI": [
#                 "Chatbots, virtual assistants, dialogue systems",
#                 "Multi-turn conversations, context management",
#                 "Tools: Rasa, DialoGPT, ChatGPT API"
#             ],
#             "LLM - Code Generation": [
#                 "GitHub Copilot-style systems, code explanation",
#                 "Code understanding, syntax-aware generation",
#                 "Tools: CodeT5, InCoder, StarCoder"
#             ]
#         },
#         "resources": {
#             "Specialized Courses": [
#                 "Medical Image Analysis - Coursera",
#                 "Self-Driving Cars Specialization - Coursera"
#             ],
#             "Domain Papers": [
#                 "Recent conference papers from CVPR, NeurIPS, ACL"
#             ]
#         }
#     },
#     "Phase 7.5: Audio Processing & Speech AI": {
#         "duration": "3-4 months",
#         "topics": {
#             "Audio Fundamentals": [
#                 "Digital signal processing basics",
#                 "Fourier transforms, spectrograms",
#                 "Audio feature extraction (MFCC, mel-scale)",
#                 "Audio preprocessing and augmentation"
#             ],
#             "Speech Recognition (ASR)": [
#                 "Traditional approaches: HMMs, GMMs",
#                 "Deep learning: CTC, attention-based models",
#                 "End-to-end systems: Listen, Attend, Spell",
#                 "Modern ASR: Whisper, Wav2Vec2, Conformer"
#             ],
#             "Speech Synthesis (TTS)": [
#                 "Concatenative synthesis",
#                 "Parametric synthesis: WaveNet, Tacotron",
#                 "Neural vocoders: HiFi-GAN, MelGAN",
#                 "Modern TTS: VALL-E, Bark, ElevenLabs-style"
#             ],
#             "Audio Understanding": [
#                 "Music information retrieval",
#                 "Audio classification and tagging",
#                 "Sound event detection",
#                 "Emotion recognition from speech"
#             ]
#         },
#         "resources": {
#             "Libraries": [
#                 "librosa, soundfile, pyaudio",
#                 "torchaudio, speechbrain",
#                 "ESPnet, fairseq",
#                 "Coqui TTS, Mozilla DeepSpeech"
#             ],
#             "Datasets": [
#                 "LibriSpeech, Common Voice",
#                 "VCTK, LJ Speech",
#                 "AudioSet, FreeSound"
#             ]
#         }
#     },    
#     "Phase 8: Advanced Research Techniques": {
#         "duration": "4-5 months",
#         "topics": {
#             "For Computer Vision": [
#                 "Self-supervised learning: Contrastive learning, masked image modeling",
#                 "Few-shot learning: Prototypical networks, meta-learning",
#                 "Domain adaptation: Transfer between different visual domains",
#                 "Interpretability: Grad-CAM, attention visualization, saliency maps"
#             ],
#             "For LLMs": [
#                 "Training optimizations: Distributed training, memory optimization",
#                 "Inference optimization: Model compression, efficient serving",
#                 "Safety and alignment: Constitutional AI, bias mitigation",
#                 "Tool use: Function calling, API integration"
#             ],
#             "Common Advanced Topics": [
#                 "Neural Architecture Search (NAS)",
#                 "Federated learning",
#                 "Continual learning",
#                 "Robustness and adversarial training"
#             ]
#         },
#         "resources": {
#             "Advanced Courses": [
#                 "Advanced Deep Learning - MIT",
#                 "Research Methods in ML - Stanford"
#             ],
#             "Cutting-edge Papers": [
#                 "Latest papers from arXiv",
#                 "Conference proceedings"
#             ]
#         }
#     },
#     "Phase 8.2: Video Processing & Understanding": {
#         "duration": "4-5 months",
#         "topics": {
#             "Video Fundamentals": [
#                 "Video formats, codecs, frame rates",
#                 "Temporal relationships in video",
#                 "Video preprocessing and augmentation",
#                 "3D convolutions vs 2D + temporal"
#             ],
#             "Action Recognition": [
#                 "Two-stream networks",
#                 "3D CNNs: C3D, I3D, R(2+1)D",
#                 "Transformer-based: Video Transformer, TimeSformer",
#                 "Self-supervised video representation learning"
#             ],
#             "Video Object Detection & Tracking": [
#                 "Temporal consistency in detection",
#                 "Multi-object tracking (MOT)",
#                 "Video instance segmentation",
#                 "Real-time processing considerations"
#             ],
#             "Video Generation & Editing": [
#                 "Video prediction and generation",
#                 "Style transfer for video",
#                 "Video inpainting and completion",
#                 "Deepfakes and face swapping (ethical considerations)"
#             ],
#             "Advanced Video Applications": [
#                 "Video summarization",
#                 "Video question answering",
#                 "Video captioning and description",
#                 "Sports analytics and surveillance"
#             ]
#         },
#         "resources": {
#             "Libraries": [
#                 "OpenCV, MoviePy, FFmpeg",
#                 "PyTorch Video, Detectron2",
#                 "MMAction2, SlowFast",
#                 "Decord, torchvision"
#             ],
#             "Datasets": [
#                 "Kinetics, UCF-101, HMDB-51",
#                 "ActivityNet, Something-Something",
#                 "YouTube-8M, AVA"
#             ]
#         }
#     },

#     "Phase 8.3: Multimodal AI Systems": {
#         "duration": "4-5 months",
#         "topics": {
#             "Vision-Language Models": [
#                 "CLIP and its variants",
#                 "ALIGN, DALL-E, DALL-E 2",
#                 "Flamingo, BLIP, InstructBLIP",
#                 "GPT-4V, LLaVA, MiniGPT-4"
#             ],
#             "Audio-Visual Learning": [
#                 "Cross-modal retrieval",
#                 "Audio-visual synchronization",
#                 "Sound source localization",
#                 "Lip reading and speech enhancement"
#             ],
#             "Multimodal Generation": [
#                 "Text-to-image: Stable Diffusion, Midjourney",
#                 "Text-to-video: Runway, Pika Labs approaches",
#                 "Text-to-audio: MusicLM, AudioLDM",
#                 "Unified multimodal generation"
#             ],
#             "Multimodal Understanding": [
#                 "Visual question answering (VQA)",
#                 "Image/video captioning",
#                 "Multimodal reasoning and common sense",
#                 "Embodied AI and robotics applications"
#             ]
#         },
#         "resources": {
#             "Models": [
#                 "OpenAI CLIP, DALL-E APIs",
#                 "Stability AI models",
#                 "HuggingFace multimodal models",
#                 "Google Bard/Gemini"
#             ],
#             "Papers": [
#                 "CLIP, ALIGN, Flamingo",
#                 "DALL-E series, Stable Diffusion",
#                 "Recent vision-language papers"
#             ]
#         }
#     },    
    
#     "Phase 8.5: Retrieval-Augmented Generation (RAG)": {
#         "duration": "2-3 months",
#         "topics": {
#             "RAG Fundamentals": [
#                 "Information retrieval basics",
#                 "Vector databases and similarity search",
#                 "Dense vs sparse retrieval",
#                 "Embedding models for retrieval"
#             ],
#             "RAG Architecture Components": [
#                 "Document chunking strategies",
#                 "Vector indexing and storage",
#                 "Retrieval mechanisms",
#                 "Generation with retrieved context"
#             ],
#             "Advanced RAG Techniques": [
#                 "Hybrid retrieval (dense + sparse)",
#                 "Re-ranking and filtering",
#                 "Multi-hop reasoning",
#                 "Self-RAG and adaptive retrieval"
#             ],
#             "RAG Optimization": [
#                 "Query expansion and reformulation",
#                 "Context compression",
#                 "Retrieval evaluation metrics",
#                 "End-to-end fine-tuning"
#             ]
#         },
#         "resources": {
#             "Tools & Libraries": [
#                 "LangChain, LlamaIndex",
#                 "Chroma, Pinecone, Weaviate",
#                 "FAISS, Elasticsearch",
#                 "HuggingFace Transformers"
#             ],
#             "Papers": [
#                 "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
#                 "Dense Passage Retrieval",
#                 "FiD: Fusion-in-Decoder"
#             ]
#         }
#     },    
#     "Phase 9: Research Skills & Paper Implementation": {
#         "duration": "4-6 months",
#         "topics": {
#             "CV Paper Reading": [
#                 "Foundational: LeNet, AlexNet, ResNet, 'Attention Is All You Need'",
#                 "Recent: Vision Transformers, CLIP, DALL-E 2, Stable Diffusion",
#                 "Venues: CVPR, ICCV, ECCV, NeurIPS, ICLR"
#             ],
#             "LLM Paper Reading": [
#                 "Foundational: Transformer, GPT series, BERT, T5",
#                 "Recent: InstructGPT, ChatGPT, GPT-4, Constitutional AI",
#                 "Venues: ACL, EMNLP, ICLR, NeurIPS, ICML"
#             ],
#             "Implementation Projects": [
#                 "Reproduce 2-3 CV papers from scratch",
#                 "Reproduce 2-3 LLM papers from scratch",
#                 "Create novel combinations of existing techniques",
#                 "Build end-to-end applications"
#             ]
#         },
#         "resources": {
#             "Paper Resources": [
#                 "Papers with Code",
#                 "arXiv.org",
#                 "Conference websites"
#             ],
#             "Implementation Guides": [
#                 "Annotated implementations",
#                 "YouTube paper walkthroughs"
#             ]
#         }
#     },
#     "Phase 9.2: Edge AI & Mobile Deployment": {
#         "duration": "3-4 months",
#         "topics": {
#             "Model Optimization for Edge": [
#                 "Quantization: INT8, INT4, binary networks",
#                 "Pruning: structured and unstructured",
#                 "Knowledge distillation",
#                 "Neural architecture search for efficiency"
#             ],
#             "Mobile AI Frameworks": [
#                 "TensorFlow Lite, TensorFlow.js",
#                 "Core ML (iOS), ML Kit (Android)",
#                 "ONNX Runtime, OpenVINO",
#                 "PyTorch Mobile, MediaPipe"
#             ],
#             "Hardware-Specific Optimization": [
#                 "CPU optimization (NEON, AVX)",
#                 "GPU optimization (Metal, OpenCL)",
#                 "NPU/TPU utilization",
#                 "Memory management on mobile"
#             ],
#             "Real-world Applications": [
#                 "Real-time camera processing",
#                 "On-device speech recognition",
#                 "Offline translation systems",
#                 "AR/VR applications"
#             ]
#         },
#         "resources": {
#             "Tools": [
#                 "TensorFlow Lite Converter",
#                 "Core ML Tools",
#                 "ONNX optimization tools",
#                 "Mobile profiling tools"
#             ],
#             "Platforms": [
#                 "Android Studio ML Kit",
#                 "Xcode Core ML",
#                 "Flutter ML plugins"
#             ]
#         }
#     },    
#     "Phase 9.5: Agentic AI Systems": {
#         "duration": "4-5 months",
#         "topics": {
#             "Agent Architecture": [
#                 "Planning and reasoning systems",
#                 "Memory management in agents",
#                 "Tool use and function calling",
#                 "Multi-step task decomposition"
#             ],
#             "Agent Frameworks": [
#                 "ReAct (Reasoning + Acting)",
#                 "Chain-of-Thought prompting",
#                 "Tree of Thoughts",
#                 "AutoGPT-style autonomous agents"
#             ],
#             "Multi-Agent Systems": [
#                 "Agent communication protocols",
#                 "Collaborative problem solving",
#                 "Role-based agent specialization",
#                 "Consensus and coordination mechanisms"
#             ],
#             "Agent Safety & Control": [
#                 "Goal alignment in agents",
#                 "Containment and sandboxing",
#                 "Human oversight integration",
#                 "Robustness testing"
#             ]
#         },
#         "resources": {
#             "Frameworks": [
#                 "LangGraph, CrewAI",
#                 "AutoGen, MetaGPT",
#                 "OpenAI Assistants API",
#                 "Custom agent implementations"
#             ],
#             "Papers": [
#                 "ReAct: Synergizing Reasoning and Acting",
#                 "Generative Agents",
#                 "Constitutional AI papers"
#             ]
#         }
#     },    
#     "Phase 10: Original Research & Specialization": {
#         "duration": "6+ months",
#         "topics": {
#             "Research Areas at the Intersection": [
#                 "Vision-Language Models: The future of AI",
#                 "Multimodal reasoning: Combining visual and textual understanding",
#                 "Embodied AI: Connecting vision, language, and robotics",
#                 "Scientific applications: Using both CV and LLM for research"
#             ],
#             "Build Research Portfolio": [
#                 "GitHub with high-quality implementations",
#                 "Technical blog posts",
#                 "Open-source contributions",
#                 "Conference submissions",
#                 "Collaboration with research groups"
#             ]
#         },
#         "resources": {
#             "Research Communities": [
#                 "ML Twitter/X community",
#                 "Research group collaborations",
#                 "Conference attendance"
#             ],
#             "Publishing Venues": [
#                 "Top-tier conferences",
#                 "Workshops",
#                 "arXiv preprints"
#             ]
#         }
#     },
#     "Phase 10.2: AI Ethics & Responsible AI": {
#         "duration": "2-3 months",
#         "topics": {
#             "Bias and Fairness": [
#                 "Types of bias in ML systems",
#                 "Fairness metrics and trade-offs",
#                 "Bias detection and mitigation techniques",
#                 "Algorithmic auditing"
#             ],
#             "Explainable AI (XAI)": [
#                 "LIME, SHAP for model interpretation",
#                 "Attention visualization",
#                 "Counterfactual explanations",
#                 "Model-agnostic explanation methods"
#             ],
#             "Privacy-Preserving ML": [
#                 "Differential privacy",
#                 "Federated learning",
#                 "Homomorphic encryption",
#                 "Secure multi-party computation"
#             ],
#             "AI Safety & Alignment": [
#                 "Robustness testing",
#                 "Adversarial examples and defenses",
#                 "AI alignment principles",
#                 "Red teaming and safety evaluation"
#             ]
#         },
#         "resources": {
#             "Libraries": [
#                 "IBM AI Fairness 360",
#                 "Microsoft Fairlearn",
#                 "Google What-If Tool",
#                 "Alibi, InterpretML"
#             ],
#             "Guidelines": [
#                 "Partnership on AI guidelines",
#                 "IEEE Standards for AI",
#                 "EU AI Act implications"
#             ]
#         }
#     },
#     "Phase 10.3: Domain-Specific Applications": {
#         "duration": "4-6 months (choose specialization)",
#         "topics": {
#             "Healthcare AI": [
#                 "Medical imaging: radiology, pathology, dermatology",
#                 "Drug discovery and molecular modeling",
#                 "Electronic health records analysis",
#                 "Clinical decision support systems"
#             ],
#             "Finance & FinTech": [
#                 "Algorithmic trading and risk management",
#                 "Fraud detection and prevention",
#                 "Credit scoring and loan approval",
#                 "Regulatory compliance (KYC, AML)"
#             ],
#             "Scientific AI": [
#                 "Climate modeling and environmental science",
#                 "Materials science and chemistry",
#                 "Astronomy and space exploration",
#                 "Biology and genomics"
#             ],
#             "Creative AI": [
#                 "Art and design generation",
#                 "Music composition and production",
#                 "Creative writing assistance",
#                 "Game development and procedural generation"
#             ],
#             "Industrial AI": [
#                 "Predictive maintenance",
#                 "Quality control and defect detection",
#                 "Supply chain optimization",
#                 "Digital twins and simulation"
#             ]
#         },
#         "resources": {
#             "Domain-specific datasets": [
#                 "Medical: MIMIC, PhysioNet",
#                 "Finance: Quandl, Yahoo Finance",
#                 "Scientific: Kaggle competitions",
#                 "Creative: Various artistic datasets"
#             ]
#         }
#     },    
#     "Phase 10.5: Model Communication Protocol (MCP) Integration": {
#         "duration": "2-3 months",
#         "topics": {
#             "MCP Server Development": [
#                 "Understanding MCP architecture",
#                 "Server implementation patterns",
#                 "Resource and tool definitions",
#                 "Client-server communication protocols"
#             ],
#             "Custom Tool Integration": [
#                 "Building domain-specific tools",
#                 "API integration patterns",
#                 "Database connectivity",
#                 "External service orchestration"
#             ],
#             "MCP Best Practices": [
#                 "Security considerations",
#                 "Performance optimization",
#                 "Error handling and recovery",
#                 "Testing and validation"
#             ],
#             "Advanced MCP Features": [
#                 "Streaming responses",
#                 "Batch operations",
#                 "State management",
#                 "Multi-tenant architectures"
#             ]
#         },
#         "resources": {
#             "Documentation": [
#                 "Official MCP specification",
#                 "Anthropic MCP documentation",
#                 "Community examples and templates"
#             ],
#             "Implementation": [
#                 "MCP SDK libraries",
#                 "Reference implementations",
#                 "Integration patterns",
#                 "Testing frameworks"
#             ]
#         }
#     },

#     "Phase 11: Production AI Systems": {
#         "duration": "3-4 months",
#         "topics": {
#             "MLOps & Model Deployment": [
#                 "Model versioning and registry",
#                 "CI/CD for ML pipelines",
#                 "A/B testing for models",
#                 "Model monitoring and drift detection"
#             ],
#             "Scalable AI Infrastructure": [
#                 "Distributed training systems",
#                 "Model serving at scale",
#                 "GPU cluster management",
#                 "Cost optimization strategies"
#             ],
#             "AI Safety in Production": [
#                 "Bias detection and mitigation",
#                 "Adversarial robustness",
#                 "Privacy-preserving ML",
#                 "Compliance and governance"
#             ],
#             "Integration Patterns": [
#                 "API design for AI services",
#                 "Real-time vs batch processing",
#                 "Edge deployment considerations",
#                 "Multi-model orchestration"
#             ]
#         },
#         "resources": {
#             "Platforms": [
#                 "Kubernetes, Docker",
#                 "MLflow, Kubeflow",
#                 "Weights & Biases, Neptune",
#                 "Cloud ML platforms (AWS, GCP, Azure)"
#             ],
#             "Books": [
#                 "Building Machine Learning Powered Applications",
#                 "ML Engineering - Andriy Burkov"
#             ]
#         }
#     },
#     "Phase 12: Quantum Machine Learning (Future-Ready)": {
#         "duration": "3-4 months",
#         "topics": {
#             "Quantum Computing Basics": [
#                 "Qubits, superposition, entanglement",
#                 "Quantum gates and circuits",
#                 "Quantum algorithms basics",
#                 "Quantum advantage and supremacy"
#             ],
#             "Quantum ML Algorithms": [
#                 "Variational Quantum Eigensolver (VQE)",
#                 "Quantum Approximate Optimization Algorithm (QAOA)",
#                 "Quantum neural networks",
#                 "Quantum kernel methods"
#             ],
#             "Hybrid Classical-Quantum Systems": [
#                 "Quantum feature maps",
#                 "Quantum data encoding",
#                 "Quantum-classical optimization",
#                 "Near-term quantum applications"
#             ]
#         },
#         "resources": {
#             "Platforms": [
#                 "IBM Qiskit, Google Cirq",
#                 "Microsoft Q#, AWS Braket",
#                 "PennyLane, TensorFlow Quantum"
#             ]
#         }
#     },

#     "Phase 13: Production AI Systems & MLOps": {
#         "duration": "4-5 months",
#         "topics": {
#             "MLOps & Model Deployment": [
#                 "Model versioning and registry",
#                 "CI/CD for ML pipelines",
#                 "A/B testing for models",
#                 "Model monitoring and drift detection"
#             ],
#             "Scalable AI Infrastructure": [
#                 "Distributed training systems",
#                 "Model serving at scale",
#                 "GPU cluster management",
#                 "Cost optimization strategies"
#             ],
#             "AI Safety in Production": [
#                 "Bias detection and mitigation",
#                 "Adversarial robustness",
#                 "Privacy-preserving ML",
#                 "Compliance and governance"
#             ],
#             "Integration Patterns": [
#                 "API design for AI services",
#                 "Real-time vs batch processing",
#                 "Edge deployment considerations",
#                 "Multi-model orchestration"
#             ],
#             "Advanced Production Topics": [
#                 "Model compression for production",
#                 "Multi-tenant ML systems",
#                 "Global model distribution",
#                 "Disaster recovery for AI systems"
#             ]
#         },
#         "resources": {
#             "Platforms": [
#                 "Kubernetes, Docker",
#                 "MLflow, Kubeflow",
#                 "Weights & Biases, Neptune",
#                 "Cloud ML platforms (AWS, GCP, Azure)"
#             ],
#             "Books": [
#                 "Building Machine Learning Powered Applications",
#                 "ML Engineering - Andriy Burkov",
#                 "Reliable Machine Learning"
#             ]
#         }
#     }

# }

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


# Combined roadmaps
ROADMAPS = {
    "Software Engineer": SOFTWARE_ENGINEER_ROADMAP,
    "ML Research Engineer": ML_RESEARCH_ROADMAP,
    "Quantitative Engineer/Scientist": QUANT_RESEARCH_ROADMAP
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
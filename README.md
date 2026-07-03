# 🚨 Fraud Detection System


A real-time fraud detection platform built with Apache Kafka, Spark Structured Streaming, Random Forest machine learning, Delta Lake, and hybrid rule-based fraud scoring.


## Author
**Mahmoud Najmeh**  
<img src="https://avatars.githubusercontent.com/u/78208459?u=c3f9c7d6b49fc9726c5ea8bce260656bcb9654b3&v=4" width="200px" style="border-radius: 50%;">

------------------------------------------------------------------------


## 🎯 Overview

The Fraud Detection System processes e-commerce transactions in real-time, combining deterministic fraud rules with a machine learning prediction layer to identify suspicious activity. It uses Kafka for reliable message streaming, Avro for efficient serialization, Random Forest based fraud scoring, Delta Lake storage, real-time alerts and comprehensive audit logging.

### Key Capabilities

- **Real-time Processing**: Sub-second fraud detection latency
- **Scalable Architecture**: Multi-partition Kafka topics with parallel consumers
- **Dual Format Support**: Avro binary for production efficiency, JSON for human readability
- **Rich Monitoring**: Terminal-based UI with live statistics and alert dashboard
- **Compliance Ready**: Complete audit trail logging in JSONL format
- **Stateful Processing**: In-memory caching of user profiles and transaction history
- **Fault Tolerant**: Failed message storage and recovery mechanisms
- **Hybrid Fraud Detection**: Rule-based fraud checks combined with machine learning fraud probability scoring
- **Combined Risk Score**: Weighted rule score and ML score are merged before alert generation

## ✨ Features

### Core Features

- 🚀 Real-time transaction processing with configurable batch sizes
- 🔍 5-tier fraud detection rules engine with severity scoring
- 🤖 Machine learning fraud prediction using a Random Forest model with fallback scoring
- 👤 User profile management with dynamic risk scoring
- 📊 Live monitoring dashboard built with Rich library
- 📝 Comprehensive audit logging with three-tier approach:
  - `fraud_audit.log` - Transaction-level audit trail (365-day retention)
  - `gdpr_deletions.log` - GDPR erasure tracking with 7-year retention (2555 days)
  - `verification.log` - Real-time metrics validation (90-day retention)
  - Daily rotation with compression for all logs
- ⏱️ **Delta Lake Time Travel & Versioning**:
  - `versionAsOf` - Query historical data snapshots by version number
  - `timestampAsOf` - Query data as it existed at any point in time
  - `history()` - Full version log with operation metadata
  - `VACUUM` - Physical deletion of old Parquet files for GDPR compliance
  - 300+ versions tracked with complete audit trail
- 🔄 Stateful stream processing with in-memory user profile cache
- 🧠 Combined risk scoring from rules and ML prediction before Kafka alert publishing
- 🛡️ Schema validation using Avro schemas
- 🐳 Fully dockerized Kafka infrastructure with Schema Registry and Kafka UI

### Technical Features

- **Multi-process architecture**: Separate processes for producers, consumers, and monitors
- **Idempotent producers**: Exactly-once semantics with transactional guarantees
- **Compacted topics**: User profiles stored with log compaction for latest state
- **Failed message recovery**: Automatic storage of failed messages for later reprocessing
- **Graceful shutdown**: Signal handlers for clean process termination
- **Comprehensive logging**: Loguru with rotation, compression, and audit log separation

## 🏗 Architecture


### Machine Learning Pipeline

```text
                 Historical Transactions
                         │
                         ▼
                 Feature Engineering
                         │
                         ▼
             Random Forest Model Training
                         │
                         ▼
                Model Serialization (.pkl)
                         │
                         ▼
                 ML Fraud Predictor
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
     Fraud Probability         Rule Risk Score
            │                         │
            └────────────┬────────────┘
                         ▼
               Combined Risk Score
                         │
                         ▼
                 Kafka Fraud Alert
                         │
                         ▼
                     Dashboard
```

The fraud detector enriches each transaction with user profile and transaction history, applies deterministic rules, calculates an ML fraud probability, merges both signals into a combined risk score, publishes alerts back to Kafka and stores alert events in Delta Lake.

### Machine Learning Workflow

The following architecture illustrates the complete machine learning lifecycle, including offline model training, feature engineering, model serialization, and real-time inference integrated with the streaming fraud detection pipeline.

### Machine Learning Architecture

<img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/15c07caf-016c-4980-b3b5-4c4b0c37de2e" />

### System Architecture Diagram

<img width="10016" height="4613" alt="Image" src="https://github.com/user-attachments/assets/db5fd6a0-f02c-4028-9028-3e5db1b9b336" />

### Data Flow Sequence Diagram

<img width="5601" height="5365" alt="Image" src="https://github.com/user-attachments/assets/9095546e-f89a-40ff-98de-7c53db330968" />

### Fraud Detection Rules Flow

<img width="5609" height="8854" alt="Image" src="https://github.com/user-attachments/assets/d932ff76-231c-4688-94b2-7eafe65558d5" />

### Component Interaction Diagram

<img width="4424" height="4408" alt="Image" src="https://github.com/user-attachments/assets/d7fc05e0-fd24-466d-b6be-2e9ab4341878" />

### State Management Diagram

<img width="4909" height="5333" alt="Image" src="https://github.com/user-attachments/assets/34629640-4f9b-45c3-b8e4-6f6acb7b34ea" />

### Deployment Architecture

<img width="7044" height="1815" alt="Image" src="https://github.com/user-attachments/assets/6aa970d2-65f5-4186-ad57-4c9cffc36a0d" />

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- 4GB RAM minimum available

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/MN10101/fraud-detection-system-kafak.git
cd fraud-detection-system-kafka

# 2. Install dependencies using uv
uv sync

# 3. Start Kafka infrastructure (broker, schema registry, UI)
docker compose up -d

# 4. Wait for services to be ready (approximately 30 seconds)
sleep 30

# 5. Create Kafka topics with proper configurations
python -m fraud_detection.main setup

# 6. Run the complete system (all components)
python -m fraud_detection.main run --mode all

## 📁 Project Structure


FRAUD-DETECTION-SYSTEM/
├── .pytest_cache/
├── .venv/
├── failed_messages/
├── htmlcov/
├── logs/
│   ├── audit/                
│   ├── app.log                
│   ├── app.*.log.gz           
│   ├── audit.log              
│   ├── audit.*.log.gz         
│   ├── error.log              
│   ├── fraud_audit.log        
│   ├── gdpr_deletions.log    
│   ├── verification.log       
│   └── error.*.log.gz         
├── scripts/
│   └── setup_topics.sh
├── src/
│   └── fraud_detection/
│       ├── __pycache__/
│       ├── __init__.py
│       ├── main.py
│       ├── config/
│       │   ├── settings.py
│       │   └── logger_config.py
│       ├── consumers/
│       │   ├── alert_consumer.py
│       │   ├── audit_consumer.py
│       │   └── fraud_detector.py
│       ├── models/
│       │   └── data_models.py
│       ├── monitoring/
│       │   └── kafka_monitor.py
│       ├── processors/
│       │   ├── enrichment_processor.py
│       │   ├── fraud_rules_engine.py
│       │   └── ml_fraud_predictor.py
│       ├── producers/
│       │   ├── transaction_producer.py
│       │   └── user_profile_producer.py
│       ├── schemas/
│       │   ├── fraud_alert.avsc
│       │   ├── transaction.avsc
│       │   └── user_profile.avsc
│       └── utils/
│           ├── avro_serializer.py
│           └── helpers.py
├── tests/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_alert_consumer_mock.py
│   ├── test_audit_consumer_mock.py
│   ├── test_avro_serializer.py
│   ├── test_enrichment_processor.py
│   ├── test_fraud_detection.py
│   ├── test_fraud_detector_mock.py
│   ├── test_fraud_rules_engine_more.py
│   ├── test_helpers.py
│   ├── test_ml_fraud_predictor.py
│   ├── test_producers.py
│   └── test_user_profile_producer_mock.py
├── .env
├── .gitignore
├── .python-version
├── docker-compose.yml
├── pyproject.toml
├── read_alerts.py
├── README.md
└── uv.lock                

🔍 Troubleshooting
# Common Issues and Solutions
Kafka broker not starting:
# Check Docker container status
docker ps -a

# View Kafka logs
docker logs fraud-detection-system-kafka-1

# Complete reset
docker compose down -v
docker compose up -d

# Topics not created:
Verify setup script ran correctly
python -m fraud_detection.main setup

# Manually create topics
./scripts/setup_topics.sh

# Check if topics exist
docker exec fraud-detection-system-kafka-1 /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Consumer lag (messages piling up):
Check consumer group status
docker exec fraud-detection-system-kafka-1 /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group fraud-detector-group \
  --describe

# Reset consumer group offset to latest
docker exec fraud-detection-system-kafka-1 /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group fraud-detector-group \
  --topic transactions \
  --reset-offsets --to-latest \
  --execute

# Schema Registry connection issues:
Verify Schema Registry is running
curl http://localhost:8081/subjects

# Check registered schemas
curl http://localhost:8081/subjects/transactions-value/versions

# Logs not appearing:
Check logs directory permissions
ls -la logs/

# View real-time logs
tail -f logs/app.log

# Check audit logs
cat logs/audit/$(date +%Y-%m-%d).jsonl | jq .

# Port conflicts:
Check if ports are in use
lsof -i :9092  # Kafka
lsof -i :8080  # Kafka UI
lsof -i :8081  # Schema Registry
```
### Audit Log Verification

After running the system, verify the Delta Lake-style audit logs:

```bash
# Check fraud audit trail
wc -l logs/fraud_audit.log

# Verify GDPR deletion tracking
cat logs/gdpr_deletions.log

# View real-time metrics
tail -f logs/verification.log

# Verify audit files are being written
tail -f logs/fraud_audit.log
tail -f logs/gdpr_deletions.log
tail -f logs/verification.log

# Check GDPR deletion was triggered
grep "GDPR_ERASURE" logs/gdpr_deletions.log
```

## 🧪 Testing

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src/fraud_detection --cov-report=html

# Run specific test file
pytest tests/test_fraud_detection.py -v
```

<img width="1503" height="327" alt="Image" src="https://github.com/user-attachments/assets/e2acdd0c-d108-41c6-99f9-82d88f6186aa" />



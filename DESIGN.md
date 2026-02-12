# MemoraAI — System Design

## Overview
MemoraAI is a memory-aware learning system that predicts forgetting risk at the topic level and generates personalized revision content using AI. The system continuously adapts based on student performance and revision behavior.

## Data Sources
- Study session logs
- Quiz and test scores
- Revision history
- Time gap since last exposure
- Topic difficulty level

## Memory Prediction Model (ML)
The memory prediction module estimates the probability that a student will forget a specific concept.

### Inputs:
- Time since last revision
- Past performance on the concept
- Frequency of past mistakes
- Topic difficulty

### Approach:
- Supervised learning model (e.g., Logistic Regression / LSTM / Bayesian Knowledge Tracing)
- Outputs a forgetting risk score for each topic

This enables dynamic, student-specific forgetting curves instead of static schedules.

## Knowledge State Modeling
Each student has a continuously updated mastery score per topic.  
This knowledge state reflects:
- Current understanding
- Stability of memory
- Risk of forgetting

## GenAI Content Engine
Based on the predicted forgetting risk, the GenAI engine generates:
- Recall-based questions
- Mini quizzes
- Scenario-based problems
- Concept reinforcement prompts

Content difficulty adapts to the student’s mastery level.

## Decision Engine
The decision engine prioritizes topics with the highest forgetting risk and generates a **personalized daily revision plan**, balancing:
- Time availability
- Exam proximity
- Cognitive load

## Feedback Loop
1. Student attempts AI-generated revision tasks
2. Performance data is collected
3. Models update forgetting predictions
4. Future revision plans improve automatically

This creates a self-improving learning system.

## User Flow Example
1. A NEET aspirant studies Biology today
2. MemoraAI predicts a 72% forgetting risk for Genetics concepts in 4 days
3. The system schedules targeted recall questions before forgetting occurs
4. Student responses update the model
5. Revision plans become more accurate over time

## Evaluation Metrics
- Retention improvement percentage
- Recall accuracy over time
- Reduction in revision time
- Prediction accuracy of forgetting events

## Scalability
MemoraAI can integrate with:
- Existing EdTech platforms
- Schools and universities
- Competitive exam preparation institutes
- Corporate upskilling systems

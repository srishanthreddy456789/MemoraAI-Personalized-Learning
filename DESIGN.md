# System Design – MemoraAI

## Data Sources
- Study logs
- Quiz scores
- Revision history

## Memory Prediction Model (ML)
Predicts forgetting probability using:
- Time gap since last revision
- Past performance
- Topic difficulty

## Knowledge State Modeling
Maintains mastery score per topic for each student.

## GenAI Engine
Generates:
- Recall questions
- Mini quizzes
- Scenario-based problems

## Decision Engine
Creates personalized daily revision plan.

## Feedback Loop
Student responses update the model for better predictions over time.

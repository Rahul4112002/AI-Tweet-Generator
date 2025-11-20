from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import operator
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Specialized LLMs for each stage
generator_llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.9,
    api_key=os.getenv('GROQ_API_KEY')
)

evaluator_llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.3,
    api_key=os.getenv('GROQ_API_KEY')
)

optimizer_llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.7,
    api_key=os.getenv('GROQ_API_KEY')
)

# Evaluation schema
class TweetEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(
        ..., description="Final evaluation result."
    )
    feedback: str = Field(
        ..., description="Detailed feedback for the tweet."
    )

structured_evaluator_llm = evaluator_llm.with_structured_output(
    TweetEvaluation
)

# State definition
class TweetState(TypedDict):
    topic: str
    tweet: str
    evaluation: Literal["approved", "needs_improvement"]
    feedback: str
    iteration: int
    max_iteration: int
    tweet_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]

def generate_tweet(state: TweetState):
    messages = [
        SystemMessage(content="You are a funny and clever Twitter/X influencer who creates viral, original tweets with emojis and hashtags."),
        HumanMessage(content=f"""
Write a short, original, and hilarious tweet about: "{state['topic']}"

Requirements:
🚫 Do NOT use question-answer format or colon structures (like "Me:" or "Person:")
📏 Maximum 280 characters
😂 Use observational humor, irony, sarcasm, or cultural references
🎯 Think in meme logic, punchlines, or relatable takes
💬 Use simple, day-to-day conversational English
✨ Add 1-2 relevant emojis naturally within the tweet
🏷️ Include 1-3 relevant hashtags at the end
🔥 Make it scroll-stopping and memorable

Create something that would genuinely make people laugh and want to retweet. Keep it natural and conversational!
""")
    ]
    response = generator_llm.invoke(messages).content
    return {'tweet': response, 'tweet_history': [response]}

def evaluate_tweet(state: TweetState):
    messages = [
        SystemMessage(content="You are a ruthless, no-laugh-given Twitter critic. You evaluate tweets based on humor, originality, virality, and format."),
        HumanMessage(content=f"""
Evaluate this tweet: "{state['tweet']}"

Criteria:
✓ Originality - Fresh or overused?
✓ Humor - Actually funny or trying too hard?
✓ Punchiness - Short, sharp, scroll-stopping?
✓ Virality - Would people retweet this?
✓ Format - Natural tweet with emojis and hashtags?

Auto-reject if:
❌ Question-answer format
❌ Colon structures (like "Me:" or "Person:")
❌ Over 280 characters
❌ Traditional setup-punchline joke format
❌ Missing emojis or hashtags

Respond with evaluation ("approved" or "needs_improvement") and brief feedback.
""")
    ]
    response = structured_evaluator_llm.invoke(messages)
    return {
        'evaluation': response.evaluation,
        'feedback': response.feedback,
        'feedback_history': [response.feedback]
    }

def optimize_tweet(state: TweetState):
    messages = [
        SystemMessage(content="You are an expert at punching up tweets for maximum virality and humor."),
        HumanMessage(content=f"""
Improve this tweet based on feedback: "{state['feedback']}"

Topic: "{state['topic']}"
Original: {state['tweet']}

Instructions:
✍️ Re-write as a short, viral-worthy tweet
🎯 Address all feedback issues
🚫 NO question-answer or colon formats (Me:, Person:, etc.)
📏 Under 280 characters
😂 Make it funnier, punchier, more original
✨ Include natural emojis in the text
🏷️ Add 1-3 relevant hashtags at the end
💯 Keep it sharp, relatable, and conversational

Provide ONLY the improved tweet, nothing else.
""")
    ]
    response = optimizer_llm.invoke(messages).content
    iteration = state['iteration'] + 1
    return {'tweet': response, 'iteration': iteration, 'tweet_history': [response]}

def route_evaluation(state: TweetState):
    if state['evaluation'] == 'approved' or state['iteration'] >= state['max_iteration']:
        return 'approved'
    else:
        return 'needs_improvement'

# Build the graph
graph = StateGraph(TweetState)
graph.add_node('generate', generate_tweet)
graph.add_node('evaluate', evaluate_tweet)
graph.add_node('optimize', optimize_tweet)

graph.add_edge(START, 'generate')
graph.add_edge('generate', 'evaluate')
graph.add_conditional_edges(
    'evaluate',
    route_evaluation,
    {'approved': END, 'needs_improvement': 'optimize'}
)
graph.add_edge('optimize', 'evaluate')

workflow = graph.compile()

def generate_viral_tweet(topic: str, max_iteration: int = 3):
    """Generate a viral tweet using LangGraph workflow"""
    initial_state = {
        'topic': topic,
        'iteration': 0,
        'max_iteration': max_iteration
    }
    
    result = workflow.invoke(initial_state)
    
    # Format history
    history = []
    for i, (tweet, feedback) in enumerate(zip(result['tweet_history'], result['feedback_history']), 1):
        history.append({
            'iteration': i,
            'tweet': tweet,
            'feedback': feedback,
            'evaluation': 'approved' if i == len(result['tweet_history']) else 'needs_improvement'
        })
    
    return {
        'final_tweet': result['tweet'],
        'evaluation': result['evaluation'],
        'total_iterations': result['iteration'],
        'history': history,
        'topic': topic
    }

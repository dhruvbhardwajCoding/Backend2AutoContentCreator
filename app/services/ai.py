import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.schemas import GenerateRequest, GenerateResponse
from app.prompts.content import CONTENT_STRATEGY_PROMPT

def generate_video_content(request_data: GenerateRequest) -> GenerateResponse:
    # Initialize the LLM
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.7,
        max_output_tokens=2048,
        thinking_budget=0,  
    )
    
    # Force the LLM to output the exact Pydantic schema
    structured_llm = llm.with_structured_output(GenerateResponse)
    
    # Format the recent topics context
    if request_data.recentVideos:
        recent_topics_list = [f"- {vid.topic}" for vid in request_data.recentVideos]
        recent_topics_str = "\n".join(recent_topics_list)
    else:
        recent_topics_str = "No recent videos. This is the first video."
        
    # Format the prompt
    prompt_val = CONTENT_STRATEGY_PROMPT.format(
        channel_name=request_data.channel.name,
        niche=request_data.channel.niche,
        description=request_data.channel.description or "No specific description provided.",
        language=request_data.channel.language,
        duration=request_data.channel.duration,
        recent_topics=recent_topics_str
    )
    
    # Execute generation
    response = structured_llm.invoke(prompt_val)
    print(response)
    
    return response

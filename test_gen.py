import os
import sys
from dotenv import load_dotenv

# load env from backend dir just in case
load_dotenv("/home/dhruv/projects/newproject/AIbackend/.env")

from app.services.ai import generate_video_content
from app.models.schemas import GenerateRequest, ChannelConfig

def main():
    req = GenerateRequest(
        channel=ChannelConfig(
            name="Test Channel",
            niche="Motivation",
            language="en",
            duration=30,
            description="Motivational shorts about life.",
            videosPerDay=1
        ),
        recentVideos=[]
    )
    
    try:
        res = generate_video_content(req)
        print("SUCCESS!")
        print(res.model_dump_json(indent=2))
    except Exception as e:
        print("ERROR:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

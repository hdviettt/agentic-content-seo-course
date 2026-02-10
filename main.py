from dotenv import load_dotenv

load_dotenv()

from workflow import workflow

topic = input("Enter your content topic: ").strip()
if not topic:
    raise SystemExit("No topic provided.")

workflow.print_response(
    topic, 
    markdown=True, 
    show_step_details=True, 
    show_time=True, 
    show_token_usage=True, 
    stream=True
    )

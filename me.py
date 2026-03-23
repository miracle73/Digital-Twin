import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.environ.get("API_TOKEN")
)

MODEL = "gpt-4.1-nano"

SYSTEM_PROMPT = """You are Miracle Nwadiaro's digital twin — an AI that represents him professionally.
You speak in first person as Miracle. You're friendly, confident, and technical.
Keep answers concise. If someone asks something not in your knowledge, say you'd prefer they reach out to the real Miracle.

ABOUT MIRACLE:
- Full name: Nwadiaro Miracle Chukwuma
- Location: Uyo, Nigeria
- Email: nwadiaromiraclechukwuma@gmail.com
- GitHub: miracle73 | LinkedIn: nwadiaro-miracle | Portfolio: mirack.site
- Education: B.Eng. Electrical and Electronics Engineering, Federal University of Technology Owerri (2015-2021), Second Class Upper (4.20/5.00)

CURRENT ROLE:
- Machine Learning Engineer / AI Engineer at Safeguardmedia (June 2024 - Present)
- Architecting scalable AI solutions for real-time disease detection using computer vision and deep learning
- Building advanced deepfake detection systems using transformer-based architectures and multi-modal analysis
- Implementing MLOps pipelines for model versioning, monitoring, and automated deployment

PAST EXPERIENCE:
- ML Intern at Start Innovation Hub (Nov 2023 - June 2024) — hands-on ML model development, data preprocessing, feature engineering
- Software Developer at DevCareer (Sep 2022 - Sep 2023) — algorithmic solutions for automated assessment systems, security protocols
- Software Developer Intern at Distrobird (May 2020 - Aug 2020) — payment processing systems

TECHNICAL SKILLS:
- AI/ML: Python, TensorFlow, PyTorch, Scikit-learn, Keras, HuggingFace Transformers
- LLM Tech: OpenAI API, LangChain, Vector databases (Pinecone, Chroma), RAG systems
- Agent Frameworks: LangGraph, CrewAI, AutoGen, multi-agent orchestration
- MLOps: Docker, Kubernetes, MLflow, Kubeflow, Apache Airflow, DVC
- Cloud: Google Cloud Platform
- Web: React, Next.js, NestJS, FastAPI, Node.js, TypeScript, TailwindCSS
- Databases: MongoDB, MySQL, vector databases

AWARDS:
- NAOC Scholarship (2016) — Nigerian Agip Oil Company Educational Grant
- Seplat JV Scholarship (2018) — Seplat Petroleum Development Company award

SOFT SKILLS: Technical writing, cross-functional collaboration, project management, mentoring
"""

# ============================================================
# TOOLS
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_technical_skills",
            "description": "Returns Miracle's detailed technical skills grouped by category",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_work_experience",
            "description": "Returns Miracle's complete work experience with details",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_projects",
            "description": "Returns Miracle's projects and open source contributions",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_contact_info",
            "description": "Returns Miracle's contact information and links",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_education",
            "description": "Returns Miracle's educational background and awards",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

def get_technical_skills():
    return json.dumps({
        "ai_ml": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "HuggingFace Transformers"],
        "llm_tech": ["OpenAI API", "LangChain", "Pinecone", "ChromaDB", "RAG systems"],
        "agent_frameworks": ["LangGraph", "CrewAI", "AutoGen", "multi-agent orchestration"],
        "mlops": ["Docker", "Kubernetes", "MLflow", "Kubeflow", "Apache Airflow", "DVC"],
        "cloud": ["Google Cloud Platform (ML services and compute)"],
        "web_dev": ["React", "Next.js", "NestJS", "FastAPI", "Node.js", "TypeScript", "TailwindCSS"],
        "databases": ["MongoDB", "MySQL", "Vector databases"],
        "languages": ["Python", "JavaScript", "TypeScript", "R"]
    })

def get_work_experience():
    return json.dumps([
        {
            "role": "Machine Learning Engineer / AI Engineer",
            "company": "Safeguardmedia",
            "period": "June 2024 - Present",
            "highlights": [
                "Architecting scalable AI solutions for real-time disease detection using computer vision",
                "Building deepfake detection systems using transformer-based architectures",
                "Implementing MLOps pipelines for model versioning, monitoring, and deployment",
                "Collaborating with agricultural experts and veterinarians for model accuracy"
            ]
        },
        {
            "role": "Machine Learning Intern",
            "company": "Start Innovation Hub",
            "period": "November 2023 - June 2024",
            "highlights": [
                "Hands-on ML model development and deployment",
                "Data preprocessing, feature engineering, model training",
                "Exploratory data analysis and research on emerging ML techniques"
            ]
        },
        {
            "role": "Software Developer",
            "company": "DevCareer (Remote)",
            "period": "September 2022 - September 2023",
            "highlights": [
                "Algorithmic solutions for automated assessment and scoring systems",
                "Security protocols and authentication frameworks",
                "Research on scalable recruitment methodologies"
            ]
        },
        {
            "role": "Software Developer Intern",
            "company": "Distrobird Software Company (Remote)",
            "period": "May 2020 - August 2020",
            "highlights": [
                "Payment processing systems",
                "Software architecture and deployment methodologies"
            ]
        }
    ])

def get_projects():
    return json.dumps({
        "deepfake_detection": {
            "status": "In Progress",
            "description": "Building advanced deepfake detection systems using transformer-based architectures and multi-modal analysis",
            "techniques": ["Facial landmark analysis", "Temporal inconsistency detection", "Transformer-based architectures", "Video authenticity verification"],
            "goal": "Real-time deepfake detection optimized for social media platforms",
            "tech": ["PyTorch", "HuggingFace Transformers", "OpenCV", "Python"]
        },
        "disease_detection_ai": {
            "status": "Production",
            "description": "Scalable AI solution for real-time disease detection and classification in agriculture using computer vision and deep learning",
            "role": "Lead ML Engineer at Safeguardmedia",
            "tech": ["TensorFlow", "Docker", "MLflow", "GCP", "FastAPI"],
            "impact": "Deployed in production with MLOps pipelines for automated model versioning and monitoring"
        },
        "automated_assessment_system": {
            "status": "Complete",
            "description": "Algorithmic solution for automated assessment and scoring in educational technology at DevCareer",
            "tech": ["Python", "Node.js", "MongoDB"],
            "impact": "Used for technical talent recruitment and assessment"
        },
        "digital_twin": {
            "status": "Live",
            "description": "AI-powered digital twin chatbot that represents me professionally using tool calling and Gradio",
            "tech": ["OpenAI API", "Gradio", "Python", "HuggingFace Spaces"],
            "url": "https://mirack.site"
        }
    })

def get_contact_info():
    return json.dumps({
        "email": "nwadiaromiraclechukwuma@gmail.com",
        "github": "https://github.com/miracle73",
        "linkedin": "https://linkedin.com/in/nwadiaro-miracle",
        "portfolio": "https://mirack.site",
        "location": "Uyo, Nigeria"
    })

def get_education():
    return json.dumps({
        "degree": "B.Eng. Electrical and Electronics Engineering",
        "institution": "Federal University of Technology Owerri",
        "period": "2015-2021",
        "gpa": "4.20/5.00",
        "class": "Second Class Upper",
        "awards": [
            {"name": "NAOC Scholarship", "year": 2016, "detail": "Nigerian Agip Oil Company Educational Grant"},
            {"name": "Seplat JV Scholarship", "year": 2018, "detail": "Seplat Petroleum Development Company award"}
        ],
        "leadership": "Technical Secretary, Nigerian Universities Engineering Students Association, FUTO Chapter (2018-2019)"
    })

tool_functions = {
    "get_technical_skills": get_technical_skills,
    "get_work_experience": get_work_experience,
    "get_projects": get_projects,
    "get_contact_info": get_contact_info,
    "get_education": get_education
}

def handle_tool_calls(response):
    tool_results = []
    for tool_call in response.choices[0].message.tool_calls:
        fn_name = tool_call.function.name
        if fn_name in tool_functions:
            result = tool_functions[fn_name]()
        else:
            result = json.dumps({"error": f"Unknown tool: {fn_name}"})
        tool_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
    return tool_results

# ============================================================
# CHAT
# ============================================================

def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=tools
    )

    if response.choices[0].message.tool_calls:
        messages.append(response.choices[0].message)
        tool_results = handle_tool_calls(response)
        messages.extend(tool_results)
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )

    return response.choices[0].message.content

# ============================================================
# GRADIO UI
# ============================================================

with gr.Blocks(title="Miracle Nwadiaro — Digital Twin") as demo:
    gr.Markdown(
        """
        # Hey, I'm Miracle 👋
        **ML Engineer / AI Engineer** — I build deepfake detectors, production ML systems, and agentic AI.  
        Ask me anything about my experience, skills, or projects.
        """
    )

    chatbot = gr.Chatbot(height=450, label="Chat with Miracle's Digital Twin")
    msg = gr.Textbox(placeholder="Ask me anything... e.g. 'What are you working on?'", label="Your message")

    with gr.Row():
        btn = gr.Button("Send", variant="primary")
        clear = gr.ClearButton([msg, chatbot], value="Clear")

    gr.Examples(
        examples=[
            "Tell me about yourself",
            "What's your tech stack?",
            "What are you currently working on?",
            "Why should we hire you as an ML Engineer?",
            "How can I contact you?"
        ],
        inputs=msg
    )

    def respond(message, chat_history):
        # Convert messages format to tuples for chat()
        history_tuples = []
        for i in range(0, len(chat_history) - 1, 2):
            if chat_history[i]["role"] == "user" and chat_history[i+1]["role"] == "assistant":
                history_tuples.append((chat_history[i]["content"], chat_history[i+1]["content"]))
        
        reply = chat(message, history_tuples)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": reply})
        return "", chat_history

    btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
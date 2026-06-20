# AI UX/UI Design Assistant

-----

   
**Description** 

An AI-powered design toolkit for product teams — generates complete UI layouts from a product description, creates accessible WCAG-rated colour palettes, and critiques uploaded UI screenshots using vision AI. Built for designers and product managers who want fast, structured feedback at any stage of the design process.

**Domain:**

UX / UI Design & Product Development

**Problem solved:** 

Early-stage design work — sketching layouts, picking an accessible colour system, getting a second opinion on a screen — usually requires a designer's time or guesswork. This tool gives product teams, founders, and developers without dedicated design support an instant, structured first pass: a layout plan broken into screens and components, a brand-appropriate colour palette with accessibility ratings built in, and an automated design critique against real UX heuristics. It's the kind of fast feedback loop that speeds up early product iteration before a human designer gets involved.

**Features**

-AI Layout Generator — describe a product in plain English, choose a platform (Mobile/Web/Desktop/Tablet) and number of screens, and get a structured screen-by-screen layout: screen names, purpose, and components with labels and design notes
-Accessible Colour Palette Generator — generate a 5-colour brand palette (Primary, Secondary, Accent, Background, Text) from a brand mood, industry, and target audience, with exact HEX/RGB values, WCAG 2.1 AA contrast ratings, and a "colours to avoid" warning
-Vision-Powered Design Critique — upload any UI screenshot (your own design, a competitor's app, any website) and receive a structured critique: overall impression, a 1–10 design maturity score, specific strengths, specific fixes, a full accessibility audit (contrast, touch targets, colour dependence, whitespace), and one prioritised next action
-Built-in example prompts on every tab so users can try the tool instantly without writing their own input
-Robust JSON handling — gracefully falls back to raw model output if structured parsing fails, so the app never crashes on a malformed LLM response

**Tech Stack**

Layer                                           Technology
LLM                                   Groq API — llama-3.3-70b-versatile
Vision model                         Groq API — meta-llama/llama-4-scout-17b-16e-instruct
Interface                                          Gradio
Secrets management                              python-dotenv

**How to Run Locally**

#### 1. Clone the repository
git clone https://github.com/somesh05/ai_design_assistant.git
cd ai_design_assistant
####  2. Create and activate a virtual environment
python -m venv designenv
source designenv/bin/activate        # Windows: designenv\Scripts\activate
####  3. Install dependencies
pip install -r requirements.txt

####  4. Add your API key
echo "GROQ_API_KEY=gsk_your_key_here" > .env

####  5. Launch the app
python app.py

The app will start a local Gradio server (typically at a temporary public link to the console if http://127.0.0.1:7860 ) and print a shareable share=True is set in demo.launch().

**Live Demo link** : https://huggingface.co/spaces/somesh05/medical-chatbot-assistant

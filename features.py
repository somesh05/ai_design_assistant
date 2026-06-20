
from prompt_engine import call_llm, call_vision, safe_json_parse
import json



def generate_layout(product_description, platform, num_screens):
    """
    Generate a UI layout plan using an LLM and return
    a human-readable summary.
    """

    system_prompt = (
        "You are a senior UX designer with 15 years of experience."
        "design clear, user centered app structure orgaised around user goals, not technical structure."
        "Always respond with valid JSON only. No extra text."
    )

    user_prompt = (
        f"Design a UI layout for: {product_description}\n"
        f"Platform: {platform}\n"
        f"Number of screens: {num_screens}\n\n"
        "Return JSON like this:\n"
        "{\n"
        '  "app_name": "name of the app",\n'
        '  "screens": [\n'
        "    {\n"
        '      "name": "screen name like Home or Login",\n'
        '      "purpose": "what user does here in one sentence",\n'
        '      "components": [\n'
        "        {\n"
        '          "type": "Button or Text Field or Card etc",\n'
        '          "label": "example label text",\n'
        '          "notes": "short note about this component"\n'
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    response = call_llm(
        system_prompt,
        user_prompt,
        temperature=0.6
    )

    try:
        clean = response.strip()

        # Remove markdown code fences if present
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1]
            clean = clean.rsplit("```", 1)[0]

        data = json.loads(clean)

        lines = []
        lines.append(f"APP: {data.get('app_name', 'Your App')}")
        lines.append("=" * 50)

        for screen in data.get("screens", []):

            lines.append(
                f"\nSCREEN: {screen.get('name', 'Unknown')}"
            )

            lines.append(
                f"Purpose: {screen.get('purpose', 'No purpose provided')}"
            )

            lines.append("-" * 40)

            for comp in screen.get("components", []):

                lines.append(
                    f"[{comp.get('type', '?')}] "
                    f"{comp.get('label', '?')}"
                )

                lines.append(
                    f"Note: {comp.get('notes', '?')}"
                )

                lines.append("")

        return "\n".join(lines)

    except Exception:
        # If JSON parsing fails,return raw LLM output
        return response
    


#Colour Palette Advisor
def generate_colour_palette(brand_mood, industry, target_audience):
    """Generate a 5-colour accessible brand palette with hex codes and WCAG ratings."""
    system_prompt = """You are a senior brand designer and accessibility expert.
    Create colour systems that are visually compelling AND meet WCAG 2.1 AA standards.
    Provide exact hex codes, RGB values, and practical usage guidance.
    Respond with JSON ONLY. No text outside the JSON."""
    user_prompt = f"""Create a 5-colour brand palette for:
    Brand mood: {brand_mood}
    Industry: {industry}
    Target audience: {target_audience}
    Return ONLY this JSON:
    {{
    "palette_name": "creative 2-3 word name",
    "rationale": "2 sentences explaining the colour psychology choices",
    "colours": [
    {{
    "role": "Primary",
    "name": "e.g. Ocean Blue",
    "hex": "#XXXXXX",
    "rgb": "rgb(R, G, B)",
    "usage": "where to use: CTAs, key actions, brand elements",
    "wcag_on_white": "Pass AA / Fail AA / Pass AAA",
    "pair_with": "which other role it pairs well with"
    }},
    {{ "role": "Secondary", ... }},
    {{ "role": "Accent", ... }},
    {{ "role": "Background", ... }},
    {{ "role": "Text", ... }}
    ],
    "avoid": "one colour combination to never use and exactly why"
    }}"""

    raw = call_llm(system_prompt, user_prompt, temperature=0.7, max_tokens=1200)

    parsed, error = safe_json_parse(raw)

    for c in parsed.get("colours", []):
        if parsed:
            lines = []
            lines.append(f"PALETTE: {parsed.get('palette_name','—')}")
            lines.append(f"WHY: {parsed.get('rationale','—')}")
            lines.append("=" * 55)
            lines.append(f"\n{c.get('role','—').upper()}")
            lines.append(f" Name: {c.get('name','—')}")
            lines.append(f" Hex: {c.get('hex','—')}")
            lines.append(f" RGB: {c.get('rgb','—')}")
            lines.append(f" Use for: {c.get('usage','—')}")
            lines.append(f" WCAG on white: {c.get('wcag_on_white','—')}")
            lines.append(f" Pairs with: {c.get('pair_with','—')}")
            lines.append(f"\nAVOID: {parsed.get('avoid','—')}")
            return "\n".join(lines)
        else:
            return f"Palette generated:\n\n{raw}"

#Design Critique with Vision AI 
def critique_design(image_pil):
    """Analyse a UI screenshot using the vision model. Returns structured critique."""
    if image_pil is None:
        return "Please upload a UI screenshot."

    # Structured prompt — specific format = specific, actionable output
    vision_prompt = """You are a senior UX/UI design critic and accessibility auditor.
    Analyse this UI screenshot carefully. Use EXACTLY this format:

    OVERALL IMPRESSION:
    [2 sentences — first impression and overall quality assessment]

    DESIGN MATURITY RATING: [X]/10
    [One sentence justifying the score]

    WHAT WORKS WELL:
    1. [Specific element + why it works visually — name the actual component]
    2. [Another specific strength with visual evidence]
    3. [Another specific strength]

    WHAT NEEDS IMPROVEMENT:
    1. [Specific issue] fi Fix: [Exact actionable recommendation]
    2. [Specific issue] fi Fix: [Exact recommendation]
    3. [Specific issue] fi Fix: [Exact recommendation]

    ACCESSIBILITY AUDIT:- 
    Text contrast: [Pass AA / Fail AA / Cannot determine] 
    — [observation]- Touch target sizes: [Adequate / Too small] 
    — [observation]- Visual hierarchy: [Clear / Unclear] — [why]
    - Colour dependence: [Yes / No] — [does design rely only on colour to convey info?]
    - Whitespace: [Good / Too tight / Too loose] — [observation]

    ONE PRIORITY FIX:
    [Most important change — name the exact element, exact change, and why it has most impact]"""

    return call_vision(image_pil, vision_prompt)
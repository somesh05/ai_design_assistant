
import gradio as gr

from features import (
    generate_layout,
    generate_colour_palette,
    critique_design
)

# ==================================================
# BUILD APP
# ==================================================

with gr.Blocks(title="AI Design Assistant") as app:

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    gr.Markdown("""
# 🎨 Generative AI UX/UI Design Assistant

AI-powered design tools for:
- UI Layout Generation
- Colour Palette Creation
- Design Critique with Vision AI
""")

    # --------------------------------------------------
    # TABS CONTAINER
    # --------------------------------------------------

    with gr.Tabs():

        # ==================================================
        # TAB 1 - LAYOUT GENERATOR
        # ==================================================

        with gr.Tab("Layout Generator"):

            gr.Markdown(
                "### Describe your product and get a complete UI layout"
            )

            product_in = gr.Textbox(
                label="What is your product?",
                placeholder="e.g. A mobile banking app for university students",
                lines=3
            )

            with gr.Row():

                platform_in = gr.Dropdown(
                    choices=[
                        "Mobile",
                        "Web",
                        "Desktop",
                        "Tablet"
                    ],
                    value="Mobile",
                    label="Platform"
                )

                screens_in = gr.Slider(
                    minimum=1,
                    maximum=5,
                    value=3,
                    step=1,
                    label="Number of Screens"
                )

            layout_btn = gr.Button(
                "Generate Layout",
                variant="primary"
            )

            layout_out = gr.Textbox(
                label="Generated UI Layout",
                lines=25,
                    )

            gr.Examples(
                examples=[
                    [
                        "A mobile fitness app for beginners wanting daily workout reminders",
                        "Mobile",
                        3
                    ],
                    [
                        "A web dashboard for freelancers to track invoices",
                        "Web",
                        4
                    ],
                    [
                        "A tablet app for nurses to view patient records",
                        "Tablet",
                        2
                    ],
                    [
                        "A mobile food delivery app for busy families",
                        "Mobile",
                        4
                    ]
                ],
                inputs=[
                    product_in,
                    platform_in,
                    screens_in
                ]
            )

            layout_btn.click(
                fn=generate_layout,
                inputs=[
                    product_in,
                    platform_in,
                    screens_in
                ],
                outputs=layout_out
            )

        # ==================================================
        # TAB 2 - COLOUR PALETTE
        # ==================================================

        with gr.Tab("Colour Palette"):

            gr.Markdown(
                "### Describe your brand and get 5 colours with HEX codes"
            )

            mood_in = gr.Textbox(
                label="Brand Mood",
                placeholder="e.g. calm, trustworthy, innovative"
            )

            industry_in = gr.Dropdown(
                choices=[
                    "Healthcare",
                    "Finance & Banking",
                    "Education",
                    "Fitness & Wellness",
                    "Technology & SaaS",
                    "Retail & E-commerce",
                    "Food & Hospitality",
                    "Travel",
                    "Legal & Professional",
                    "Other"
                ],
                value="Technology & SaaS",
                label="Industry"
            )

            audience_in = gr.Textbox(
                label="Target Audience",
                placeholder="e.g. young professionals aged 25-35 who value simplicity"
            )

            palette_btn = gr.Button(
                "Generate Palette",
                variant="primary"
            )

            palette_out = gr.Textbox(
                label="Generated Colour Palette",
                lines=22,
                
            )

            gr.Examples(
                examples=[
                    [
                        "trustworthy, calm, professional",
                        "Finance & Banking",
                        "adults 30-55 managing savings"
                    ],
                    [
                        "energetic, bold, motivating",
                        "Fitness & Wellness",
                        "people 18-35 new to fitness"
                    ],
                    [
                        "clean, minimal, clinical",
                        "Healthcare",
                        "doctors and nurses"
                    ],
                    [
                        "friendly, playful, bright",
                        "Education",
                        "university students"
                    ]
                ],
                inputs=[
                    mood_in,
                    industry_in,
                    audience_in
                ]
            )

            palette_btn.click(
                fn=generate_colour_palette,
                inputs=[
                    mood_in,
                    industry_in,
                    audience_in
                ],
                outputs=palette_out
            )

        # ==================================================
        # TAB 3 - DESIGN CRITIQUE
        # ==================================================

        with gr.Tab("Design Critique"):

            gr.Markdown("""
### Upload any UI screenshot and get a design critique

Take a screenshot of:
- Your own design
- A competitor's design
- Any website or mobile app

The Vision AI will analyse the image and provide feedback.
""")

            with gr.Row():

                with gr.Column(scale=1):

                    image_in = gr.Image(
                        label="Upload Screenshot",
                        type="pil",
                        height=350
                    )

                    critique_btn = gr.Button(
                        "Critique This Design",
                        variant="primary"
                    )

                    gr.Markdown("""
**Screenshot Tips**

**Mac:** Cmd + Shift + 4

**Windows:** Win + Shift + S
""")

                with gr.Column(scale=1):

                    critique_out = gr.Textbox(
                        label="AI Design Critique",
                        lines=26,
                        
                    )

            critique_btn.click(
                fn=critique_design,
                inputs=image_in,
                outputs=critique_out
            )

# ==================================================
# LAUNCH
# ==================================================

if __name__ == "__main__":

    app.launch(
        server_port=7860,
        share=False
    )

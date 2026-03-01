from PIL import Image, ImageDraw, ImageFont

def create_placeholder(filename, text, size=(800, 600)):
    img = Image.new('RGB', size, color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    # Just draw text in the center
    d.text((50, size[1]//2), text, fill=(255, 255, 0))
    img.save(filename)

create_placeholder('dashboard_insightforge.png', 'Placeholder: Dashboard (KPIs + trend line + top contributors)')
create_placeholder('query_growth_region.png', 'Placeholder: Example query ("Which region drove growth last quarter?")')
create_placeholder('insight_cards.png', 'Placeholder: Insight cards (recommendations)')

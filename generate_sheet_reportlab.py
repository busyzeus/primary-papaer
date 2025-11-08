from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def draw_ruled_lines(c, y, line_height, font_name, font_size):
    ascent = pdfmetrics.getAscent(font_name)
    descent = pdfmetrics.getDescent(font_name)

    # Baseline is at y
    c.setStrokeColorRGB(0, 0, 1) # Blue
    c.line(c._pagesize[0] * 0.1, y, c._pagesize[0] * 0.9, y)

    # Topline
    top_line_y = y + ascent * font_size / 1000
    c.line(c._pagesize[0] * 0.1, top_line_y, c._pagesize[0] * 0.9, top_line_y)

    # Midline
    mid_line_y = y + (ascent / 2) * font_size / 1000
    c.setDash(1, 1)
    c.setStrokeColorRGB(1, 0, 0) # Red
    c.line(c._pagesize[0] * 0.1, mid_line_y, c._pagesize[0] * 0.9, mid_line_y)
    c.setDash([], 0)

def generate_handwriting_sheet_reportlab(text, font_path, font_name, line_height, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    pdfmetrics.registerFont(TTFont(font_name, font_path))
    font_size = 28
    c.setFont(font_name, font_size)

    margin = width * 0.1
    x = margin
    y = height - margin - line_height

    words = text.split()
    remaining_words = list(words)

    while y > margin and remaining_words:
        draw_ruled_lines(c, y, line_height, font_name, font_size)
        current_line = ""
        
        while remaining_words:
            word = remaining_words[0]
            if c.stringWidth(current_line + " " + word) < width - 2 * margin:
                if current_line:
                    current_line += " "
                current_line += word
                remaining_words.pop(0)
            else:
                break
        
        c.drawString(x, y, current_line)
        y -= line_height

    c.save()

if __name__ == '__main__':
    lyric = "I was a ghost, I was alone. Given the throne, I didn't know how to believe. I was the queen that I'm meant to be. I lived two lives, tried to play both sides. But I couldn't find my own place Called a problem child 'cause I got too wild. But now that's how I'm getting paid on stage. I'm done hidin', now I'm shinin' like I'm born to be. We dreamin' hard, we came so far, now I'll believe We're goin' up, up, up, it's our moment"
    font_path = "C:\\Windows\\Fonts\\SCRIPTBL.TTF"
    font_name = "ScriptMT"
    line_height = 40
    output_path = "handwriting_sheet_reportlab.pdf"
    generate_handwriting_sheet_reportlab(lyric, font_path, font_name, line_height, output_path)

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTFont as FT_TTFont

def get_font_metrics(font_path, font_name, font_size):
    # Get ascent and descent from reportlab
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    ascent = pdfmetrics.getAscent(font_name)
    descent = pdfmetrics.getDescent(font_name)

    # Convert to points
    ascent_in_points = (ascent * font_size) / 1000.0
    descent_in_points = (descent * font_size) / 1000.0

    # Get x-height from fontTools
    x_height_in_points = 0
    try:
        ft_font = FT_TTFont(font_path)
        if "OS/2" in ft_font:
            os2_table = ft_font["OS/2"]
            if hasattr(os2_table, 'sxHeight'):
                x_height_font_units = os2_table.sxHeight
            elif hasattr(os2_table, 'sTypoAscender'):
                # Fallback: use sTypoAscender as an approximation for x-height
                # This is not ideal, but a reasonable approximation when sxHeight is missing
                x_height_font_units = os2_table.sTypoAscender * 0.5 # A common approximation
                print(f"Warning: 'sxHeight' not found. Approximating x-height using sTypoAscender for {font_path}.")
            else:
                print(f"Warning: Neither 'sxHeight' nor 'sTypoAscender' found in OS/2 table for {font_path}.")
                x_height_font_units = 0 # Default to 0 if no approximation can be made
            
            if x_height_font_units > 0:
                # Convert font units to points
                units_per_em = ft_font['head'].unitsPerEm
                x_height_in_points = (x_height_font_units / units_per_em) * font_size
            else:
                x_height_in_points = 0
        else:
            print(f"OS/2 table not found in {font_path}. Cannot determine x-height precisely.")
    except Exception as e:
        print(f"Error processing font file {font_path} with fontTools: {e}")

    return ascent_in_points, descent_in_points, x_height_in_points

def draw_ruled_lines(c, baseline_y, baseline_to_midline_distance, midline_to_topline_distance, x_height_in_points, width, margin):
    # Baseline
    c.setStrokeColorRGB(0, 0, 1) # Blue
    c.line(margin, baseline_y, width - margin, baseline_y)

    # Midline
    mid_line_y = baseline_y + baseline_to_midline_distance
    c.setDash(1, 1) # Dashed line
    c.setStrokeColorRGB(1, 0, 0) # Red
    c.line(margin, mid_line_y, width - margin, mid_line_y)
    c.setDash([], 0) # Solid line for subsequent lines

    # Topline
    top_line_y = mid_line_y + midline_to_topline_distance
    c.setStrokeColorRGB(0, 0, 1) # Blue
    c.line(margin, top_line_y, width - margin, top_line_y)

def generate_handwriting_sheet_reportlab(text, font_path, font_name, font_size,
                                        baseline_to_midline_distance, midline_to_topline_distance,
                                        line_set_gap, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    ascent_in_points, descent_in_points, x_height_in_points = get_font_metrics(font_path, font_name, font_size)

    pdfmetrics.registerFont(TTFont(font_name, font_path))
    c.setFont(font_name, font_size)

    margin = width * 0.1
    x = margin
    
    # Calculate the total height of one ruled line set
    line_set_height = baseline_to_midline_distance + midline_to_topline_distance

    # Starting y position for the first baseline
    y = height - margin - line_set_height

    words = text.split()
    remaining_words = list(words)

    while y > margin: # Loop until the bottom margin is reached
        draw_ruled_lines(c, y, baseline_to_midline_distance, midline_to_topline_distance, x_height_in_points, width, margin)
        
        if remaining_words:
            current_line = ""
            
            # Adjust text_y to align x-height with the midline
            mid_line_y = y + baseline_to_midline_distance
            text_y = mid_line_y - x_height_in_points
            
            while remaining_words:
                word = remaining_words[0]
                test_line = current_line + (" " if current_line else "") + word
                if c.stringWidth(test_line) < width - 2 * margin:
                    if current_line:
                        current_line += " "
                    current_line += word
                    remaining_words.pop(0)
                else:
                    break
            
            c.drawString(x, text_y, current_line)
        
        y -= (line_set_height + line_set_gap) # Move to the next line set

    c.save()

if __name__ == '__main__':
    lyric = "I was a ghost, I was alone. Given the throne, I didn't know how to believe. I was the queen that I'm meant to be. I lived two lives, tried to play both sides. But I couldn't find my own place Called a problem child 'cause I got too wild. But now that's how I'm getting paid on stage. I'm done hidin', now I'm shinin' like I'm born to be. We dreamin' hard, we came so far, now I'll believe We're goin' up, up, up, it's our moment"
    font_path = "C:\\Windows\\Fonts\\SCRIPTBL.TTF"
    font_name = "ScriptMT"
    
    # New customizable parameters
    font_size = 28
    baseline_to_midline_distance = 10 # Distance from baseline to midline
    midline_to_topline_distance = 10  # Distance from midline to topline
    line_set_gap = 15                 # Vertical gap between ruled sets

    output_path = "handwriting_sheet_reportlab.pdf"
    generate_handwriting_sheet_reportlab(lyric, font_path, font_name, font_size,
                                        baseline_to_midline_distance, midline_to_topline_distance,
                                        line_set_gap, output_path)

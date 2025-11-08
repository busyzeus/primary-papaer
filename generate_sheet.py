from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def draw_primary_ruled_lines(self, line_height):
        self.set_draw_color(0, 0, 255)  # Blue for top and bottom lines
        self.set_line_width(0.5)
        
        y = self.t_margin
        while y < self.h - self.b_margin:
            # Top line
            self.line(self.l_margin, y, self.w - self.r_margin, y)
            
            # Dashed midline
            self.set_draw_color(255, 0, 0)  # Red for dashed midline
            self.set_line_width(0.2)
            self.set_dash_pattern(dash=1, gap=1)
            self.line(self.l_margin, y + line_height / 2, self.w - self.r_margin, y + line_height / 2)
            self.set_dash_pattern(dash=0, gap=0) # reset dash pattern
            
            # Bottom line
            self.set_draw_color(0, 0, 255)  # Blue for top and bottom lines
            self.set_line_width(0.5)
            self.line(self.l_margin, y + line_height, self.w - self.r_margin, y + line_height)

            y += line_height * 1.5 # Move to the next set of lines with some spacing

def generate_handwriting_sheet(text, font_path, font_name, line_height, output_path):
    pdf = PDF()
    pdf.add_page()
    try:
        pdf.add_font(font_name, "", font_path)
    except RuntimeError as e:
        if "Can't open file" in str(e):
            print(f"Font file not found at {font_path}. Please provide a valid path.")
            return

    pdf.draw_primary_ruled_lines(line_height)

    # Set font size based on line height
    pdf.set_font(font_name, "", 1) # Set font size to 1 to get normalized metrics
    font_metrics = pdf.fonts[pdf.font_family]
    ascent = font_metrics.desc.ascent
    descent = font_metrics.desc.descent
    font_size = line_height * 1000 / (ascent - descent)
    pdf.set_font(font_name, "", font_size)

    # Set text position
    x = pdf.l_margin
    y = pdf.t_margin + line_height

    words = text.split(' ')
    current_line = ''
    for word in words:
        if pdf.get_string_width(current_line + ' ' + word) < pdf.w - pdf.l_margin - pdf.r_margin:
            current_line += ' ' + word
        else:
            pdf.text(x, y, current_line.strip())
            current_line = word
            y += line_height * 1.5
    pdf.text(x, y, current_line.strip())

    pdf.output(output_path)

if __name__ == '__main__':
    lyric = "I was a ghost, I was alone. Given the throne, I didn't know how to believe. I was the queen that I'm meant to be. I lived two lives, tried to play both sides. But I couldn't find my own place Called a problem child 'cause I got too wild"
    font_path = "C:\\Windows\\Fonts\\SCRIPTBL.TTF"
    font_name = "ScriptMT"
    line_height = 20
    output_path = "handwriting_sheet.pdf"
    generate_handwriting_sheet(lyric, font_path, font_name, line_height, output_path)
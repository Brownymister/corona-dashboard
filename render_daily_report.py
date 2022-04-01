from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pathlib

def render_daily_report_image(new_infektion, new_death, total_infektion, total_death, inzidence, myresult_yesterday) -> None: 
    width = 1200
    height = 1000
    img = Image.new('RGB', (width, height), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    font_normal = ImageFont.truetype("./Prompt,Space_Mono/Prompt/Prompt-LightItalic.ttf", 70)
    font_smal = ImageFont.truetype("./Prompt,Space_Mono/Prompt/Prompt-LightItalic.ttf", 20)

    size = 0.2
    infectionPerDayChart = Image.open('./static/InfectionPerDayChart.png')
    infectionPerDayChart = infectionPerDayChart.resize((round(infectionPerDayChart.size[0]*size), round(infectionPerDayChart.size[1]*size)))
    incidence = Image.open('./static/incidence.png')
    incidence = incidence.resize((round(incidence.size[0]*size), round(incidence.size[1]*size)))
    arrow_up = Image.open('./arrows/arrow_up.png')
    arrow_down = Image.open('./arrows/arrow_down.png')

    now = datetime.now()

    today = now.strftime("%d_%m_%Y")
    d.text((width/2,20), str(today),font=font_smal, fill="#000", anchor="ms")

    d.text((100,80), str(total_infektion),font=font_normal, fill="#000")
    d.text((100,160), "Infektionen seit Beginn",font=font_smal,fill="#000")

    d.text((width - 300,80), "+"+str(new_infektion),font=font_normal, fill="#000")
    d.text((width - 300,160), "Neuinfektionen",font=font_smal,fill="#000")

    d.text((100,200), str(total_death),font=font_normal, fill="#000")
    d.text((100,280), "Todesfälle seit Beginn",font=font_smal,fill="#000")

    d.text((width - 300,200), "+"+str(new_death),font=font_normal, fill="#000")
    d.text((width - 300,280), "neue Todesfälle",font=font_smal,fill="#000")

    d.text((width/2, 400), "Ø"+str(inzidence), font=font_normal, fill="#000", anchor="ms")
    d.text((width/2,430), "7-Tage-Inzi­denz",font=font_smal,fill="#000", anchor="ms")

    if int(myresult_yesterday[0][0]) >= new_infektion:
        img.paste(arrow_down, (width - 380, 100))
    else:
        img.paste(arrow_up, (width - 380, 100))
    img.paste(incidence, (600, 500))
    img.paste(infectionPerDayChart, (10, 500))

    img.save(str(pathlib.Path("render_daily_report.py").parent.resolve())+'/daily_reports/daily_report_'+str(today)+'.png')

# render_daily_report_image(1123, 123, 25463, 14, 12389)
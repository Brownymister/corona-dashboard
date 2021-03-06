"""
.. module:: render_daily_report

.. moduleauthor:: Julian `Brownymister` <Brownymister@gmail.com>

"""

from PIL import Image, ImageDraw, ImageFont
import pathlib

from numpy import average
# module
from .date import Date


class Daily_report:

    image = None
    drawn_image = None
    font_normal = None
    font_smal = None

    arrow_up_image = Image.open('./arrows/arrow_up.png')
    arrow_down_image = Image.open('./arrows/arrow_down.png')

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.image = Image.new('RGB', (width, height), color=(255, 255, 255))
        self.drawn_image = ImageDraw.Draw(self.image)
        self.font_normal = ImageFont.truetype(
            "./font/Prompt-LightItalic.ttf", 70)
        self.font_smal = ImageFont.truetype(
            "./font/Prompt-LightItalic.ttf", 20)

        self.daily_report_plot = Image.open('./static/daily_report_plot.png')

    def render_daily_report_image(self, new_infektion, new_death, total_infektion, total_death, inzidence, sum_last_7D,save_folder) -> None:
        self.resize_size_of_chart(new_size=0.55)

        today = Date().get_formatted_date()
        self.draw_corona_infos_to_image(
            new_infektion, new_death, total_infektion, total_death, inzidence, today)

        self.add_arrow_to_image(new_infektion, (sum_last_7D/7))
        self.add_chart_to_image()

        self.image.save(str(pathlib.Path("render_daily_report.py").parent.resolve())+save_folder+'/daily_report_'+str(today)+'.png')

    def resize_size_of_chart(self, new_size):
        self.daily_report_plot = self.daily_report_plot.resize(
            (round(self.daily_report_plot.size[0]*new_size),
             round(self.daily_report_plot.size[1]*new_size))
        )

    def draw_corona_infos_to_image(self, new_infektion, new_death, total_infektion, total_death, inzidence, today):
        self.drawn_image.text((self.width/2, 20), str(today),
                              font=self.font_smal, fill="#000", anchor="ms")

        self.drawn_image.text((100, 80), str(
            total_infektion), font=self.font_normal, fill="#000")
        self.drawn_image.text(
            (100, 160), "Infektionen seit Beginn", font=self.font_smal, fill="#000")

        self.drawn_image.text((self.width - 300, 80), "+" +
                              str(new_infektion), font=self.font_normal, fill="#000")
        self.drawn_image.text((self.width - 300, 160),
                              "Neuinfektionen", font=self.font_smal, fill="#000")

        self.drawn_image.text((100, 200), str(total_death),
                              font=self.font_normal, fill="#000")
        self.drawn_image.text(
            (100, 280), "Todesf??lle seit Beginn", font=self.font_smal, fill="#000")

        self.drawn_image.text((self.width - 300, 200), "+" +
                              str(new_death), font=self.font_normal, fill="#000")
        self.drawn_image.text(
            (self.width - 300, 280), "neue Todesf??lle", font=self.font_smal, fill="#000")

        self.drawn_image.text((self.width/2, 400), "??"+str(inzidence),
                              font=self.font_normal, fill="#000", anchor="ms")
        self.drawn_image.text((self.width/2, 430), "7-Tage-Inzi??denz",
                              font=self.font_smal, fill="#000", anchor="ms")

    def add_arrow_to_image(self, new_infektion, average_infection_of_week):
        average_of_week_is_greater_than_todays_new_infection = average_infection_of_week >= new_infektion
        if average_of_week_is_greater_than_todays_new_infection:
            self.image.paste(self.arrow_down_image, (self.width - 380, 100))
        else:
            self.image.paste(self.arrow_up_image, (self.width - 380, 100))

    def add_chart_to_image(self):
        self.image.paste(self.daily_report_plot, (50, 450))
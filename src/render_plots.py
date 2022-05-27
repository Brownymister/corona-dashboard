import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import numpy as np
# modules
from src.db import Db
from src.date import Date


class RenderPlot:
    """class to render plot
    """
    def __init__(self) -> None:
        self.dates = []
        self.all_new_infections = []
        self.smothed_new_infections = []
        self.all_new_deaths = []
        self.total_infections = []
        self.total_deaths = []
        self.incidence = []

        self.sort_data()

    def sort_data(self):
        db = Db()

        all_data_from_db = db.get_all_data_from_db()
        
        for day in all_data_from_db:
            self.dates.append(day[0])
            self.all_new_infections.append(int(day[1]))
            self.smothed_new_infections.append(int(day[7])/7)
            self.all_new_deaths.append(int(day[6]))
            self.total_infections.append(int(day[2]))
            self.total_deaths.append(int(day[5]))
            self.incidence.append(float(day[4]))

        self.render_and_save_main_plot()

    def render_and_save_main_plot(self):
        fig, axs = plt.subplots(3, 1,figsize=(15,10))
        st = plt.suptitle(f"Corona-dashboard data for Germany at {Date().get_formatted_date()} - Brownymister mrbrowny.de", fontsize='xx-large')
        top_ax, middle_ax, bottom_ax = axs

        top_ax.set_ylim([0, max(self.smothed_new_infections)+20000])
        top_ax.plot(self.dates, self.all_new_infections,color="#df5729",linewidth=1.0,label='Daily new infections')
        top_ax.plot(self.dates ,self.smothed_new_infections,color="#df5729",linewidth=3.0,label='Smoothed new infections')
        top_ax.set_ylabel("Daily new infections")
        top_ax.grid(True)
        top_ax.legend()
        top_ax.set_title('data per day')

        ax0 = top_ax.twinx()
        ax0.set_ylabel('Daily new deaths', color='tab:blue',)
        ax0.plot(self.dates, self.all_new_deaths,label="Daily new deaths")
        ax0.legend(loc="upper center")

        middle_ax.plot(self.dates, self.total_infections,color='#df5729',label='total infections')
        middle_ax.set_yticks(np.arange(0, max(self.total_infections), 4000000))
        middle_ax.set_ylabel("infections and deaths in millions")
        middle_ax.grid(True)
        middle_ax.set_title('total data')
        middle_ax.legend()

        ax1 = middle_ax.twinx()
        ax1.set_ylabel('total deaths', color='#df5729')
        ax1.plot(self.dates, self.total_deaths,color='tab:blue',label="total deaths")
        ax1.legend(loc="upper center")

        bottom_ax.plot(self.dates, self.incidence ,label="incendence")
        bottom_ax.grid(True)
        bottom_ax.set_ylabel("Daily incidence")
        bottom_ax.legend()
        bottom_ax.set_title('incedence')

        for ax in axs.flat:
            ax.set(xlabel='days')

        fig.tight_layout()

        st.set_y(0.95)
        fig.subplots_adjust(top=0.9)

        plt.savefig("./static/corona-german.png")
        plt.close()

    def render_plot_daily_report(self):

        all_data_in_db = Db().get_all_data_from_db()

        dates = []
        new_infections = []
        smothed_new_infections = []
        incidence = []

        for day in all_data_in_db:
            dates.append(day[0])
            new_infections.append(int(day[1]))
            incidence.append(float(day[4]))
            smothed_new_infections.append(round(int(day[7])/7))

        fig, ax = plt.subplots(1, 2,figsize=(20, 10))

        ax[0].set_yticks(np.arange(0, int(max(new_infections)), 100000)) 
        ax[0].plot(dates, new_infections,color="#df5729",linewidth=1.0,label="Neue Infektionen pro Tag")
        ax[0].plot(dates ,smothed_new_infections,color="#df5729",linewidth=3.0,label='Durchschnitt der letzten 7 Tage an neuen Infektionen')
        ax[0].grid(True)
        ax[0].legend()

        ax[1].set_yticks(np.arange(0, int(max(incidence)), 100)) 
        ax[1].plot(dates ,incidence,color="tab:blue",linewidth=1.0,label='Durchschnitt der neuen Infektionen')
        ax[1].grid(True)
        ax[1].legend()

        ax[0].set_title("Neue Infektionen pro Tag")
        ax[1].set_title("Inzidenz pro Tag")

        fig.tight_layout()
        plt.savefig("./static/daily_report_plot.png")
        plt.close()

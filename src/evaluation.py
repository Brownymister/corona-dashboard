"""
.. module:: evaluation

.. moduleauthor:: Julian `Brownymister` <Brownymister@gmail.com>

"""

import numpy as np
import matplotlib.pyplot as plt

class Evaluation:

    averages = []
    classes = ['Mondays', 'Tuesdays', "Wednesdays",
                   "Thursdays", "Fridays", "Saturdays", "Sundays"]

    def evaluate_average_per_day(self, infections:list):
        """calculates the average of new infections per day

        Args:
            infections (list): list of new infections per day
        """
        infections = list(self.split_array_to_smaler_arrays(infections, 7))

        week = {
            "Mondays": [],
            "Tuesdays": [],
            "Wednesdays": [],
            "Thursdays": [],
            "Fridays": [],
            "Saturdays": [],
            "Sundays": [],
        }

        for i in infections:
            week['Wednesdays'].append(i[0])
            if len(i) >= 2:
                week['Thursdays'].append(i[1])
            if len(i) >= 3:
                week['Fridays'].append(i[2])
            if len(i) >= 4:
                week['Saturdays'].append(i[3])
            if len(i) >= 5:
                week['Sundays'].append(i[4])
            if len(i) >= 6:
                week['Mondays'].append(i[5])
            if len(i) >= 7:
                week['Tuesdays'].append(i[6])

        for class_ in range(len(self.classes)):
            average = round(self.calculate_average(self.classes[class_], week), 5)
            self.averages.append(average)

    def split_array_to_smaler_arrays(self,array:list, number_of_parts:int):
        for i in range(0, len(array), number_of_parts):
            yield array[i:i + number_of_parts]

    def calculate_average(self, weekday:str, week:object) -> float:
        """calculates the averagde by given weekday

        Args:
            weekday (str): 
            week (object): 

        Returns:
            float: average of infections at weekday
        """
        weekday_sum = 0
        for i in week[weekday]:
            weekday_sum += int(i)
        weekday_average = weekday_sum / len(week[weekday])
        return weekday_average

    def save_average_as_plot(self,filename:str="./static/average.png") -> None: 
        """
        requires the evaluate_average_per_day() function to run in the same instance.
        The images are saved in .png Files.
        If not specified, the file name is "./staic/average.png".
        """
        if self.averages != []:
            objects = set(self.classes)
            y_pos = np.arange(len(objects))
            performance = self.averages

            plt.figure(3,figsize=(12,6))
            plt.bar(y_pos, performance, align='center')
            plt.xticks(y_pos, objects)
            plt.ylabel('Infection')
            plt.title('Average of infections peer weekday')

            plt.savefig(filename)    
        else:
            print("ERROR: average not calculated; To save, the function evaluation.evaluate_average_per_day() must be executed")
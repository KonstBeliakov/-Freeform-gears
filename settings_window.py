import tkinter as tk

import image_read
import settings
from main_window import MainWindow
from widgets import *


class SettingsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings")

        self.main_window = None

        self.widgets = [
            TextEntry(self, 'Radius of random figure', str(settings.r)),
            TextEntry(self, 'Number of points', str(settings.n)),
            TextEntry(self, 'Speed', str(settings.speed)),
            ChoiceYesNo(self, "Use random figure", settings.random_generated),
            TextEntry(self, 'k1 ("period")', str(settings.perlin_noise_params[0])),
            TextEntry(self, 'k2 ("amplitude")', str(settings.perlin_noise_params[1])),
            TextEntry(self, 'Filename', str(settings.filename)),
            TextEntry(self, 'Line thickness', str(settings.line_thickness)),
            TextEntry(self, 'surface stretching', str(settings.surface_stretching)),
            ChoiceYesNo(self, 'Closed surface contour', settings.closed_surface_contour),
            TextEntry(self, 'Average surface height', str(settings.average_surface_height)),
            ChoiceYesNo(self, 'Generate a pair for a gear', settings.pair_of_gear),
            TextEntry(self, 'Figure filename (svg file)', str(settings.figure_filename)),
            TextEntry(self, 'Surface filename (svg file)', str(settings.surface_filename)),
        ]

        button = tk.Button(self, text="Run", command=self.on_run)
        button.pack()

    def apply_settings(self):
        try:
            settings.r = int(self.widgets[0].get())
            settings.n = int(self.widgets[1].get())
            settings.speed = float(self.widgets[2].get())
            settings.random_generated = self.widgets[3].get()

            # k1, k2
            settings.perlin_noise_params[0] = float(self.widgets[4].get())
            settings.perlin_noise_params[1] = float(self.widgets[5].get())

            settings.filename = self.widgets[6].get()
            settings.line_thickness = int(self.widgets[7].get())

            settings.surface_stretching = float(self.widgets[8].get())

            settings.closed_surface_contour = self.widgets[9].get()
            settings.average_surface_height = int(self.widgets[10].get())
            settings.pair_of_gear = self.widgets[11].get()

            # figure_filename, surface_filename
            settings.figure_filename = self.widgets[12].get()
            settings.surface_filename = self.widgets[13].get()

            if not settings.random_generated:
                image_read.img_to_obj()

        except Exception as exc:
            error_label = tk.Label(self, text=f"Incorrect settings parameters: {exc}", fg="#f00")
            error_label.pack()
            return False
        else:
            return True

    def on_run(self):
        if self.apply_settings():
            self.destroy()
            self.main_window = MainWindow()
            while True:
                self.main_window.update()

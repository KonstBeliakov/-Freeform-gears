import tkinter as tk

import image_read
import settings
from main_window import MainWindow


class SettingsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings")

        self.main_window = None

        self.texts = ['radius of random figure', 'number of point', 'speed', 'random generated figure (y/n)',
                      'k1 ("period")', 'k2 ("amplitude")', 'filename', 'line thickness', 'surface stretching',
                      'closed surface contour (y/n)', 'average surface height', 'generate a pair for a gear (y/n)',
                      'Save svg of the figure to:', 'Save svg of the surface to:']

        entrys_values = [str(settings.r), str(settings.n), str(settings.speed), str(settings.random_generated),
                         str(settings.perlin_noise_params[0]), str(settings.perlin_noise_params[1]),
                         str(settings.filename), str(settings.line_thickness), str(settings.surface_stretching),
                         str(settings.closed_surface_contour), str(settings.average_surface_height),
                         str(settings.pair_of_gear), settings.figure_filename, settings.surface_filename]

        self.labels = [tk.Label(self, text=text) for text in self.texts]
        self.entrys = [tk.Entry(self) for i in range(len(self.texts))]

        for i in range(len(self.texts)):
            self.labels[i].grid(row=i, column=0)
            self.entrys[i].insert(0, entrys_values[i])
            self.entrys[i].grid(row=i, column=1)

        button = tk.Button(self, text="Run", command=self.change_text)
        button.grid(row=len(self.texts), column=0)

    def apply_settings(self):
        try:
            settings.r = int(self.entrys[0].get())
            settings.n = int(self.entrys[1].get())
            settings.speed = float(self.entrys[2].get())
            true_strings = ['True', 'y', 'Y', '1', 'yes', 'Yes', 'YES', 'true', 't']
            settings.random_generated = self.entrys[3].get() in true_strings
            settings.perlin_noise_params[0] = float(self.entrys[4].get())
            settings.perlin_noise_params[1] = float(self.entrys[5].get())
            settings.filename = self.entrys[6].get()
            settings.line_thickness = int(self.entrys[7].get())
            settings.surface_stretching = float(self.entrys[8].get())
            settings.closed_surface_contour = self.entrys[9].get() in true_strings
            settings.average_surface_height = int(self.entrys[10].get())

            settings.pair_of_gear = self.entrys[11].get() in true_strings

            settings.figure_filename = self.entrys[12].get()
            settings.surface_filename = self.entrys[13].get()

            if not settings.random_generated:
                image_read.img_to_obj()
        except:
            error_text = tk.Label(self, text='Incorrect settings parameters', fg='#f00')
            error_text.grid(row=len(self.texts) + 1, column=0)
            return False
        else:
            return True

    def change_text(self):
        if self.apply_settings():
            self.destroy()
            self.main_window = MainWindow()
            while True:
                self.main_window.update()

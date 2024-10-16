import sys
from tkinter import *
from tkinter import messagebox, filedialog, colorchooser
from PIL import ImageTk, Image, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.color_code = None
        self.watermark_canvas = None
        self.watermark_window = None
        self.new_img2 = None
        self.img_display = None
        self.logo_text = None
        self.y = None
        self.x = None
        self.resize_img = None
        self.new_height = None
        self.color = None
        self.font = None
        self.font_size = None
        self.text_window = None
        self.type_text = None
        self.text_to_add = None
        self.color_to_add = None
        self.font_to_add = None
        self.font_size_to_add = None
        self.first_time = None
        self.text_widgets = None
        self.logo_widgets = None
        self.resize_img2 = None
        self.image_canvas = None
        self.logo_images = None
        self.root = root
        self.root.config(bg="white")
        self.root.title("Watermark Application")
        self.files = []
        self.image_widgets = []
        self.image_labels = []
        self.first_iteration = True
        self.TEXT_X = 250
        self.TEXT_Y = 200
        self.top = None
        self.setup_main_ui()

    def choose_color(self):
        # variable to store hexadecimal code of color
        self.color = colorchooser.askcolor(title="Choose color")
        print(self.color[1])

    def setup_main_ui(self):
        canvas = Canvas(self.root, height=400, width=400, bg="white", highlightbackground="white")
        try:
            img = ImageTk.PhotoImage(Image.open('download.jpg'))
            canvas.create_image(200, 200, image=img)
            canvas.grid(column=0, row=0, padx=20)
        except FileNotFoundError:
            print("Watermark logo not found. Download your own Image and re-run.")
            canvas.create_text(200, 200, text="Watermark App", fill="Black", font=("Helvetica", 24))
            canvas.grid(column=0, row=0, padx=20)

        select_button = Button(self.root, text="Select Files", font=('Ariel', 20), command=self.open_file)
        select_button.config(bd=0, highlightbackground="white", bg='black', fg='black', pady=10, padx=10)
        select_button.grid(column=0, row=1, pady=(10, 80))

        self.root.mainloop()

    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill="white")
        alpha = Image.new('L', im.size, "white")
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file_path and file_path not in self.files:
            self.files.append(file_path)
            if self.first_iteration:
                self.render_screen()
                self.first_iteration = False
            self.display_images()

    def render_screen(self):
        self.top = Toplevel(self.root)
        self.top.config(bg="white")
        self.top.geometry("615x750")
        self.top.title("Child Window")

        top_canvas = Canvas(self.top, width=615, height=50, bg="grey", bd=0, highlightbackground="grey")
        top_canvas.grid(column=0, columnspan=6, row=0)

        Button(self.top, text="Close App", bd=0, highlightthickness=0,
               highlightbackground="grey", command=self.close).place(x=40, y=17)
        Button(self.top, text="Add Files", bd=0, highlightthickness=0,
               highlightbackground="grey", command=self.open_file).place(x=225, y=17)
        Button(self.top, text="Clear", bd=0, highlightthickness=0,
               highlightbackground="grey", command=self.clear_images).place(x=325, y=17)
        Button(self.top, text="Next >", bd=0, highlightthickness=0,
               highlightbackground="grey", command=self.next_steps).grid(column=4, columnspan=2, row=0)

    def display_images(self):

        col = 0
        row = 1

        for file in self.files:
            new_img = Image.open(file)
            width = int(new_img.size[0])
            height = int(new_img.size[1])
            self.new_height = int(round((height / width) * 125))

            resize_img = new_img.resize((125, self.new_height))
            resize_img = self.add_corners(resize_img, 15)
            new_img = ImageTk.PhotoImage(resize_img)

            image_label = Label(self.top, image=new_img, bd=0, bg="white", highlightthickness=0)
            image_label.image = new_img
            image_label.grid(column=col, columnspan=2, row=row, padx=40, pady=(40, 0))

            try:

                bin_img = Image.open('Delete-PNG-High-Quality-Image.png')
                bin_img = ImageTk.PhotoImage(bin_img)

                delete_button = Button(self.top, image=bin_img, bd=0, highlightthickness=0,
                                       command=lambda f=file: self.delete_image(f))
                delete_button.image = bin_img
                delete_button.grid(column=col, row=row + 1)
            except FileNotFoundError:
                print("No button image not found. Using built in emoji keyboard.")
                delete_button = Button(self.top, bd=0, highlightthickness=0,
                                       command=lambda f=file: self.delete_image(f), highlightcolor="white", text="❌")

                delete_button.grid(column=col, row=row + 1)

            try:
                yes_img = Image.open('green-check-mark-symbol-button-line-circle-grass-angle-logo-png-clipart.jpg')
                yes_img = ImageTk.PhotoImage(yes_img)

                yes_button = Button(self.top, image=yes_img, bd=0, highlightthickness=0,
                                    command=lambda f=file: self.watermark_image(f))
                yes_button.image = yes_img
                yes_button.grid(column=col + 1, row=row + 1)

            except FileNotFoundError:
                print("Yes button image not found. Using built in emoji keyboard.")
                yes_button = Button(self.top, bd=0, highlightthickness=0,
                                    command=lambda f=file: self.watermark_image(f), text="✅")

                yes_button.grid(column=col + 1, row=row + 1)

            self.image_widgets.append((file, image_label, delete_button, yes_button))
            self.image_labels.append(image_label)

            if col == 4:
                col = 0
                row += 2
            else:

                col += 2

    def delete_image(self, file):
        if file in self.files:
            self.files.remove(file)

        for widget in self.image_widgets:
            widget[1].destroy()
            widget[2].destroy()
            widget[3].destroy()

        if not self.files:
            self.top.destroy()
            self.first_iteration = True

        self.display_images()

    def next_steps(self):
        self.watermark_image(self.files[0])

    def watermark_image(self, file):
        self.new_img2 = Image.open(file)
        new_height = int(round((self.new_img2.size[1] / self.new_img2.size[0]) * 600))

        self.watermark_window = Toplevel(self.root)
        self.watermark_window.config(bg="white")
        self.watermark_window.geometry(f"{680}x{new_height + 180}")
        self.watermark_window.title("Watermark Window")

        self.watermark_canvas = Canvas(self.watermark_window, width=680, height=50, bg="grey",
                                       bd=0, highlightbackground="grey").grid(column=0, columnspan=6, row=0)
        Button(self.watermark_window, text="Remove Widgets", bd=0, highlightthickness=0, highlightbackground="grey",
               command=self.delete_widgets).place(x=40, y=17)
        Button(self.watermark_window, text="Add Text", bd=0, highlightthickness=0, highlightbackground="grey",
               command=self.add_it).place(x=265, y=17)
        Button(self.watermark_window, text="Add Logo", bd=0, highlightthickness=0, highlightbackground="grey",
               command=self.add_logo).place(x=365, y=17)
        Button(self.watermark_window, text="Save", bd=0, highlightthickness=0, highlightbackground="grey",
               command=self.export).place(x=550, y=17)

        self.resize_img2 = self.new_img2.resize((600, new_height))
        self.img_display = ImageTk.PhotoImage(self.resize_img2)

        self.image_canvas = Canvas(self.watermark_window, width=600, height=new_height + 30, bg="white", bd=0,
                                   highlightbackground="white")
        self.image_canvas.create_image(300, new_height/2, image=self.img_display)

        self.image_canvas.grid(column=0, columnspan=6, row=1, pady=40)

        self.logo_images = []
        self.logo_widgets = []
        self.logo_text = []
        self.text_widgets = []

        self.watermark_window.bind('<B1-Motion>', self.move_logo)
        self.watermark_window.bind('<Left>', lambda e: self.move_text(-10, 0))
        self.watermark_window.bind('<Right>', lambda e: self.move_text(10, 0))
        self.watermark_window.bind('<Up>', lambda e: self.move_text(0, -10))
        self.watermark_window.bind('<Down>', lambda e: self.move_text(0, 10))

    def move_logo(self, event):
        for widget in self.logo_widgets:
            self.image_canvas.delete(widget)
        self.logo_widgets = [
            self.image_canvas.create_image(event.x, event.y, image=image)
            for image in self.logo_images
        ]

        self.x = event.x
        self.y = event.y

    def move_text(self, dx, dy):
        self.TEXT_X += dx
        self.TEXT_Y += dy
        for text in self.text_widgets:
            self.image_canvas.move(text, dx, dy)

    def add_logo(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
        if file:
            logo_img = Image.open(file)
            self.new_height = int(round((logo_img.size[1] / logo_img.size[0]) * 124))
            self.resize_img = logo_img.resize((124, self.new_height))
            new_logo_img = ImageTk.PhotoImage(self.resize_img)

            self.logo_images = [new_logo_img]
            for image in self.logo_widgets:
                self.image_canvas.delete(image)
            self.logo_widgets = [self.image_canvas.create_image(300, 200, image=new_logo_img)]

    def add_it(self):

        fonts = [
            "Arial",
            "Courier New",
            "Times New Roman",
            "Herculanum",
            "Verdana"
        ]

        font_sizes = [
            '6', '7', '8', '9', '10', '11', '12', '14', '16', '18', '21', '24', '30', '36', '48', '60', '72'
        ]

        self.font = StringVar()
        self.font.set("Arial")

        self.font_size = StringVar()
        self.font_size.set("6")

        self.text_window = Toplevel(self.root)
        self.text_window.title("Add Text")
        type_text_label = Label(self.text_window, text="Type your text here: ")
        self.type_text = Entry(self.text_window)
        type_text_label.grid(column=0, row=0, padx=(40, 0), pady=10)
        self.type_text.grid(column=1, row=0, padx=(0, 40), pady=10)

        type_font_label = Label(self.text_window, text="Font type: ")
        font_menu = OptionMenu(self.text_window, self.font, *fonts)
        type_font_label.grid(column=0, row=1, padx=(40, 0), pady=10)
        font_menu.grid(column=1, row=1, pady=10)

        font_size_menu = OptionMenu(self.text_window, self.font_size, *font_sizes)
        font_label = Label(self.text_window, text="Font size: ")
        font_label.grid(column=0, row=2, padx=(40, 0), pady=10)
        font_size_menu.grid(column=1, row=2, pady=10)

        color_menu = Button(self.text_window, text="Select color",
                            command=self.choose_color)
        color_label = Label(self.text_window, text="Colour:")
        color_label.grid(column=0, row=3, padx=(40, 0), pady=10)
        color_menu.grid(column=1, row=3, pady=10)

        confirm_selection = Button(self.text_window, text="Confirm", command=self.show)
        confirm_selection.grid(column=1, row=4, pady=10)

        self.first_time = True

    def show(self):

        if self.type_text.get().strip() == '':
            messagebox.showwarning("Text", "Do not leave the Text field blank.")
        else:

            for text in self.logo_text:
                self.image_canvas.delete(text)

            self.logo_text.clear()
            self.text_widgets.clear()

            self.text_to_add = self.type_text.get()
            self.color_to_add = self.color[1]
            self.font_to_add = self.font.get()
            self.font_size_to_add = int(self.font_size.get())

            self.text_window.destroy()

            text = self.image_canvas.create_text(self.TEXT_X, self.TEXT_Y, text=self.text_to_add, anchor=NW,
                                                 fill=self.color_to_add, font=(self.font_to_add, self.font_size_to_add))
            self.logo_text.append(text)
            self.text_widgets.append(text)

            if self.first_time:
                messagebox.showinfo("Info", "Use the arrow keys to move the text around the image")
                self.first_time = False

    def export(self):

        try:

            file_location = filedialog.asksaveasfilename(defaultextension="png")

            final_image = self.resize_img2

            print(self.TEXT_X)
            print(self.TEXT_Y)

            increment_up = int(self.new_height / 2)

            if len(self.logo_text) > 0:
                final_image_font = ImageFont.truetype(f"{self.font_to_add.title()}.ttf", self.font_size_to_add)
                edit_image = ImageDraw.Draw(final_image)
                edit_image.text((self.TEXT_X, self.TEXT_Y), text=self.text_to_add, fill=self.color_to_add,
                                font=final_image_font)

            if len(self.logo_widgets) > 0:

                try:

                    final_image.paste(self.resize_img, (self.x - 62, self.y - increment_up))

                except NameError:

                    final_image.paste(self.resize_img, (300 - 62, 200 - increment_up))

            final_image.save(file_location)
            final_image.show()

            self.watermark_window.destroy()

        except ValueError:
            print("User clicked cancel.")

    def delete_widgets(self):
        for widget in self.logo_widgets + self.text_widgets:
            self.image_canvas.delete(widget)
        self.logo_widgets = []
        self.text_widgets = []

    def clear_images(self):
        self.files.clear()
        for widget in self.image_widgets:
            widget[1].destroy()
            widget[2].destroy()
            widget[3].destroy()
        self.image_widgets = []
        self.top.destroy()
        self.first_iteration = True

    def close(self):
        sys.exit()


if __name__ == "__main__":
    root = Tk()
    app = WatermarkApp(root)

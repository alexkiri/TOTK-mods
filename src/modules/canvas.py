import sys
from idlelib.tooltip import Hovertip
from ttkbootstrap import *
from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageOps
from configuration.settings import *
import time
import string
import random
import ttkbootstrap as ttk


def next_index(event, var, list=list, command=None):
    value = str(var.get())
    string_list = [str(item) for item in list]
    index = string_list.index(value)
    index += 1
    if index == len(list):
        index = 0
    var.set(list[index])
    if command is not None:
        command(event)


def toggle(event, var):
    if var.get() == "On":
        var.set("Off")
    else:
        var.set("On")

class Canvas_Create:
    def __init__(self):
        self.tooltip = None
        self.window = None
        self.tooltip_active = None
        self.is_Ani_running = True
        self.is_Ani_Paused = False

    def create_combobox(self, canvas,
                        text, master, description_name=None, variable=any, values=[],
                        row=40, cul=40, drop_cul=180, width=150,
                        tags=[], tag=None, command=None, is_active=True):
        # create text
        active_color_new = active_color
        if tag is not None:
            tags.append(tag)
        if is_active is False:
            active_color_new = None
        elif is_active is True:
            tags.append("active_text")
        # add outline and user-tag to the outlined text.
        outline_tag = ["outline", tag]
        # create an outline to the text.
        canvas.create_text(
                           scale(cul) + scale(1),
                           scale(row) + scale(1),
                           text=text,
                           anchor="w",
                           fill=outline_color,
                           font=textfont,
                           tags=outline_tag
                           )
        # create the text and the variable for the dropdown.
        new_variable = tk.StringVar(master=master, value=variable)
        text_line = canvas.create_text(
                                       scale(cul),
                                       scale(row),
                                       text=text,
                                       anchor="w",
                                       fill=textcolor,
                                       font=textfont,
                                       tags=tags,
                                       activefil=active_color_new
                                       )

        # create combobox
        dropdown = ttk.Combobox(
                                master=master,
                                textvariable=new_variable,
                                values=values,
                                state="readonly",
                                )

        dropdown_window = canvas.create_window(
                                               scale(drop_cul),
                                               scale(row),
                                               anchor="w",
                                               window=dropdown,
                                               width=scale(width),
                                               height=CBHEIGHT,
                                               tags=tag
                                               )
        # bind canvas
        dropdown.bind("<<ComboboxSelected>>", command)
        # attempt to make a Hovertip
        self.read_description(
                              canvas=canvas,
                              option=description_name,
                              position_list=[dropdown, text_line],
                              master=master
                              )
        canvas.tag_bind(text_line, "<Button-1>", lambda event: next_index(event, new_variable, values, command))
        row += 40
        return new_variable

    def create_checkbutton(
            self, master, canvas,
            text, description_name=None, variable=any,
            row=40, cul=40, drop_cul=180,
            tags=[], tag=None, command=None, is_active=True):
        # create text
        active_color_new = active_color
        if tag is not None:
            tags.append(tag)
        if is_active is False:
            active_color_new = None
        elif is_active is True:
            tags.append("active_text")
        # add outline and user-tag to the outlined text.
        outline_tag = ["outline", tag]
        # create an outline to the text.
        canvas.create_text(
                           scale(cul) + scale(1),
                           scale(row) + scale(1),
                           text=text,
                           anchor="w",
                           fill=outline_color,
                           font=textfont,
                           tags=outline_tag
                           )
        # create the text and the variable for the dropdown.
        new_variable = tk.StringVar(master=master, value=variable)
        text_line = canvas.create_text(
                                       scale(cul),
                                       scale(row),
                                       text=text,
                                       anchor="w",
                                       fill=textcolor,
                                       font=textfont,
                                       tags=tags,
                                       activefil=active_color_new,
                                       )

        # create checkbutton
        checkbutton = ttk.Checkbutton(
                                master=master,
                                variable=new_variable,
                                onvalue="On",
                                offvalue="Off",
                                state="readonly",
                                command=command,
                                bootstyle="success"
                                )

        checkbutton_window = canvas.create_window(
                                               scale(drop_cul),
                                               scale(row),
                                               anchor="w",
                                               window=checkbutton,
                                               tags=tag
                                               )
        # attempt to make a Hover tip
        canvas.tag_bind(text_line, "<Button-1>", lambda event: toggle(event, new_variable))
        self.read_description(
                              canvas=canvas,
                              option=description_name,
                              position_list=[checkbutton, text_line],
                              master=master
                              )
        row += 40
        return new_variable

    def create_button(
            self, master, canvas,
            btn_text, description_name=None, textvariable=None,
            row=40, cul=40, width=None, padding=None, pos="w",
            tags=[], tag=None,
            style="default", command=any,
                      ):
        # create text
        if tag is not None:
            tags.append(tag)
        # create button

        button = ttk.Button(
            master=master,
            text=btn_text,
            command=command,
            textvariable=textvariable,
            bootstyle=style,
            padding=padding
        )

        canvas.create_window(
            scale(cul),
            scale(row),
            width=scale(width*10),
            anchor=pos,
            window=button,
            tags=tags
        )

        self.read_description(
            canvas=canvas,
            option=description_name,
            position_list=[button],
            master=master
        )
        return

    def create_label(self, master, canvas,
                        text, description_name=None, font=textfont, color=textcolor, active_fill=None,
                        row=40, cul=40,
                        tags=[], tag=None, outline_tag=None, command=None
                     ):
        # create text
        if tag is not None:
            tags.append(tag)
        if command is not None and active_fill is None:
            active_fill = active_color
        # add outline and user-tag to the outlined text.
        if outline_tag is not None:
            outline_tag = [outline_tag, tag]
        # create an outline to the text.
        canvas.create_text(
                           scale(cul) + scale(1),
                           scale(row) + scale(1),
                           text=text,
                           anchor="w",
                           fill=outline_color,
                           font=font,
                           tags=outline_tag,
                           )
        # create the text and the variable for the dropdown.
        text_line = canvas.create_text(
                                       scale(cul),
                                       scale(row),
                                       text=text,
                                       anchor="w",
                                       fill=color,
                                       font=font,
                                       tags=tags,
                                       activefil=active_fill,
                                       )
        canvas.tag_bind(text_line, "<Button-1>", command)
        self.read_description(
                              canvas=canvas,
                              option=description_name,
                              position_list=[text_line],
                              master=master
                              )

    def image_Button(self, canvas,
                     row, cul, anchor="nw",
                     img_1=any, img_2=any,
                     tag_1=None, tag_2=None,
                     command=None
                     ):
        # If strings are not defined use random tags.
        if tag_1 is None:
            tag_1 = random.choices(string.ascii_uppercase +
                           string.digits, k=8)
            tag_1 = ''.join(tag_1)
        if tag_2 is None:
            tag_2 = random.choices(string.ascii_uppercase +
                           string.digits, k=8)
            tag_2 = ''.join(tag_2)
        # Trigger Animation
        canvas.create_image(scale(cul), scale(row), anchor=anchor, image=img_1, state="normal", tags=tag_1)
        canvas.create_image(scale(cul), scale(row), anchor=anchor, image=img_2, state="hidden", tags=tag_2)

        # Bind the actions for the button.
        canvas.tag_bind(tag_1, "<Enter>", lambda event: self.toggle_img(
                                                                        canvas=canvas, mode="Enter",
                                                                        tag_1=tag_1, tag_2=tag_2,
                                                                        event=event))
        canvas.tag_bind(tag_2, "<Leave>", lambda event: self.toggle_img(
                                                                        canvas=canvas, mode="Leave",
                                                                        tag_1=tag_1, tag_2=tag_2,
                                                                        event=event))
        canvas.tag_bind(tag_2, "<Button-1>", command)
        return tag_1, tag_2

    def toggle_img(self, canvas, mode, tag_1, tag_2, event=None):
        if mode.lower() == "enter":
            canvas.itemconfig(tag_1, state="hidden")
            canvas.itemconfig(tag_2, state="normal")
        if mode.lower() == "leave":
            canvas.itemconfig(tag_1, state="normal")
            canvas.itemconfig(tag_2, state="hidden")

    def read_description(self, canvas, option, position_list=list, master=any):
        if f"{option}" not in description:
            return
        for position in position_list:
            try:
                canvas_item = canvas.find_withtag(position)
                if canvas_item:
                    hover = description[f"{option}"]
                    self.create_tooltip(canvas, position, hover, master)
                    break
            except TclError as e:
                hover = description[f"{option}"]
                Hovertip(position, f"{hover}", hover_delay=Hoverdelay)

    def create_tooltip(self, canvas, position, hover, master):

        canvas.tag_bind(position, "<Enter>", lambda event: self.show_tooltip(
                                                                             event=event,
                                                                             item=position,
                                                                             tool_text=hover,
                                                                             the_canvas=canvas,
                                                                             master=master
                                                                             )
                        )

        canvas.tag_bind(position, "<Leave>", lambda event: self.hide_tooltip(event=event))
        canvas.tag_bind(position, "<Return>", lambda event: self.hide_tooltip(event))

    def show_tooltip(self, event, item, tool_text, the_canvas, master):
        bbox = the_canvas.bbox(item)
        x, y = bbox[0], bbox[1]
        x += the_canvas.winfo_rootx()
        y += the_canvas.winfo_rooty()

        master.after(50)
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x + scale(20)}+{y + scale(25)}")
        tooltip_label = tk.Label(
                                 master=self.tooltip,
                                 text=tool_text,
                                 background="gray",
                                 relief="solid",
                                 borderwidth=1,
                                 justify="left"
                                 )
        tooltip_label.pack()
        self.tooltip_active = True

    def hide_tooltip(self, event):
        self.tooltip.destroy()
        self.tooltip_active = False

    def focus(self, event):
        # Handle animations and events during those animations.
        self.is_Ani_Paused = False
        
    def un_focus(self, event):
        self.is_Ani_Paused = True

    def on_closing(self, master):
        print("Closing Window")
        self.is_Ani_running = False
        master.destroy()

    def canvas_animation(self, master, canvas):
        canvas.bind("<Enter>", self.focus)
        canvas.bind("<Leave>", self.un_focus)
        x = 0
        y = 0
        m = 1
        if sf >= 1.5:
            m *= 2
        if FPS == 0.1:
            m *= 2
        a = scale(m)
        while True:
            if self.is_Ani_running is False:
                return
            if self.is_Ani_Paused is False or get_setting("ani") in ["Off", "Disabled"]:
                if x < 1000:
                    x += m
                    canvas.move("background", -a, 0)
                    time.sleep(FPS)
                if x >= 1000:
                    if y == 0:
                        canvas.move("background", scale(200), scale(300))
                    if y < 300:
                        y += m
                        canvas.move("background", 0, -a)
                        time.sleep(FPS)
                    if y >= 300:
                        x = 0
                        y = 0
                        canvas.move("background", scale(800), 0)
            else:
                time.sleep(1)

    def get_UI_path(self, file_name, folder_name="GUI"):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            path = os.path.join(base_path, folder_name, file_name)
            if not os.path.exists(path):
                return file_name
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.dirname(base_path)
            path = os.path.join(base_path, folder_name, file_name)
            if not os.path.exists(path):
                return file_name
        return path

    def Photo_Image(self, image_path=str, is_stored=False,
                    width=None, height=None,
                    blur=None, mirror=False, flip=False,
                    auto_contrast=False, img_scale=None):

        UI_path = self.get_UI_path(image_path)
        image = Image.open(UI_path)
        if isinstance(img_scale, int) or isinstance(img_scale, float):
            width = int(width * img_scale)
            height = int(height * img_scale)
        if isinstance(width, int) and isinstance(height, int):
            image = image.resize((scale(width), scale(height)))
        if isinstance(blur, int):
            image = image.filter(ImageFilter.GaussianBlur(blur))
        if mirror is True:
            image = ImageOps.mirror(image)
        if flip is True:
            image = ImageOps.flip(image)
        if auto_contrast is True:
            image = ImageOps.autocontrast(image)
        new_photo_image = ImageTk.PhotoImage(image)

        return new_photo_image
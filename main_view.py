from tkinter import *
from tkinter import ttk
import dlib_process
from subprocess import call
from gtts import gTTS
import os
from PIL import Image, ImageTk
from twilio.rest import Client
from tempfile import TemporaryFile

class MainView(ttk.Frame):

    data_matrix = []
    image_reference_list = []
    current_option = ""
    back_option = ""
    next_option = ""
    rows = 0
    selected_items = ""
    blink_count = 0
    selected_info_image = None
    next_can_img = None
    next_can_txt = None
    curr_can_txt = None
    curr_can_img = None

    # ---- callback function for button
    def calculate(self):
        if self.app_start == True: self.get_audio_text("Please blink to select your choice.")
        self.app_start = False
        # create an object of Video Process
        self.stop_cycle = False
        self.land_mark_process = dlib_process.DlibProcess()
        # start time limited blink detection
        self.status, self.blink_count = self.land_mark_process.get_blinkcount()
        if self.status == True:
            print("==========Got Blink count: ", self.blink_count)
            self.get_next_option_onblink()
        else: print("Failed to get Blink count")

        if self.stop_cycle == False:
            root.after(100, self.calculate)

    def update(self):
        print('update function', self.blink_count)
        root.after(300, self.update)

    def get_next_option_onblink(self):
        print("In get_next_option_onblink ::::,  blink_count=  ",self.blink_count)
        for i in range(self.rows):
            print("current_option = ",self.current_option)
            if self.data_matrix[i][0] == self.current_option:
                self.next_option = self.data_matrix[i][1]
                self.back_option = self.data_matrix[i][2]
                print("In get_next_option_onblink ::::,  Back Option= ", self.back_option, ",  Current_Option  = ", self.current_option, ",  next_option=  ", self.next_option)
                if self.back_option == "meal" or self.back_option =="health_assistance" or self.back_option =="mobility_assistance" or self.back_option =="emergency" :
                    self.selected_items = ""
                    self.info_labelimg.configure(image='')

                if self.blink_count > 0:
                    if "back" in self.current_option:
                        self.selected_items = ""
                    else:self.selected_items = self.current_option
                    self.set_selected_info()

                    self.back_option = self.current_option
                    self.current_option = self.next_option

                    if self.current_option == "request":
                        text = self.back_option.replace("_", " ").title()+" Requested"
                        audio_text = "Your request for " + self.back_option.replace("_",
                                                                                       " ").title() + " has been sent. Your help is on the way. Thank you."
                        self.requested_msg.set(audio_text)
                        print("get requested msg = ", self.requested_msg.get())
                        self.get_audio_text(audio_text) # remove comment
                        if "Emergency" in text: self.send_call()
                        self.set_items(self.back_option, self.current_option, text)

                        self.stop_cycle = True
                        root.after(5000, self.set_item_mainscreen("meal"))
                    else:
                        text = self.current_option.replace("_", " ").title()
                        self.set_items(self.back_option, self.current_option, text)


                elif self.blink_count == 0:
                    if "back" in self.current_option:
                        self.selected_items = self.current_option[:-5]
                        self.set_selected_info()
                        #text = "Back"
                    if "back" in self.back_option: text = "Back"
                    else : text = self.back_option.replace("_", " ").title()
                    self.set_items(self.current_option, self.back_option, text)
                    self.current_option = self.back_option
                break


    def set_selected_info(self):
        if self.selected_items != "":
            self.selected_info.set("You Selected " + self.selected_items.replace("_"," ").title())
            self.selected_info_image = PhotoImage(file="./gif_images/" + self.selected_items + ".gif")
            self.info_labelimg.configure(image = self.selected_info_image)
            self.info_labelimg.image = self.selected_info_image

        else:
            self.selected_info.set("")
            self.info_labelimg.configure(image='')

    def get_audio_text(self, audio_text):
        language = 'en'
        myobj = gTTS(text=audio_text, lang=language, slow=False)
        myobj.save("./audio_text.mp3")
        # Playing the converted file
        call(["ffplay", "-nodisp", "-autoexit", "./audio_text.mp3"])

    def send_call(self):
        account_sid = "AC41f98e886f567f58cec9b61e2d5cbf39"
        auth_token = "e6066bc799a63a9251f687404f60dd57"
        client = Client (account_sid, auth_token)
        twilio_call = client.calls.create(to="+18056896547", from_="+18447477770", url="https://api.rcqatol.com/rentcafeapi.aspx?requesttype=twiliotest")
        print(twilio_call.status)

    # ---- read mapping file and store into matrix form
    def get_data_matrix(self):
         with open("./data_mapping", 'r') as f:
            for line in f:
                row = line.rstrip().split(', ')
                self.data_matrix.append(row)
                self.rows += 1
            return self.data_matrix, self.rows

    # -- reset texts and information
    def set_item_mainscreen(self, option):


        self.selected_items = ""
        self.selected_info.set("")
        self.requested_msg.set("")
        self.info_labelimg.configure(image='')
        self.can.delete(self.next_can_img)
        self.can.delete(self.next_can_txt )
        self.can.delete(self.curr_can_img )
        self.can.delete(self.curr_can_txt )
        self.current_option = self.data_matrix[0][0]

        self.image = PhotoImage(file="./gif_images/" + option + ".gif")
        img_height = self.image.height()
        img_width = self.image.width()
        self.curr_can_img = self.can.create_image(450, 190, anchor=CENTER, image=self.image, tags="image")
        self.curr_can_txt = self.can.create_text(img_width + 100, img_height - 175, anchor=CENTER, fill='white',
                                      font=("Times", 22, "bold"))
        self.can.itemconfigure(self.curr_can_txt, text=option.replace("_", " ").title())
        self.current_option = option
        self.stop_cycle = False


    def set_items(self, option, next_option, text):
        distx = 10
        if(next_option != ""):
            for i in range(100):
                self.can.move(self.curr_can_img, distx, 0)
                self.can.move(self.curr_can_txt, distx, 0)
                if (i == 45):
                    self.image_reference_list.append(PhotoImage(file="./gif_images/" + next_option + ".gif"))
                    self.next_can_img = self.can.create_image(-self.image_reference_list[-1].width(), self.can.winfo_height()/3, image=self.image_reference_list[-1], anchor=NW)
                    self.next_can_txt = self.can.create_text(-self.image_reference_list[-1].width() + (self.image_reference_list[-1].width() / 2), self.image_reference_list[-1].height() - 150, text=text, fill='white', font=("Times", 22, "bold"))
                if i >= 45:
                    self.can.move(self.next_can_img, distx, 0)
                    self.can.move(self.next_can_txt, distx, 0)
                root.update()  # update the display
                root.after(20)  # wait 30 ms

            self.curr_can_img = self.next_can_img
            self.curr_can_txt = self.next_can_txt

    def __init__(self, master):
        ttk.Frame.__init__(self)
        self.selected_info = StringVar()
        self.requested_msg = StringVar()
        self.app_start = True
        # ---- set initial screen
        self.data_matrix, rows = self.get_data_matrix()
        self.current_option = self.data_matrix[0][0]
        frame_style = ttk.Style()
        frame_style.configure('Black.TLabel', background="#003455")     #013243") 002366
        infostyle = ttk.Style()
        infostyle.configure('Black.TLabelframe', background="#000099")

        # ---- top frame to set help message
        top_frame = ttk.Frame(master, padding="15 15 15 15", style='Black.TLabel')
        top_frame.pack(side=TOP, fill="both")
        self.logo = PhotoImage(file="./gif_images/logo.png")
        main_label = ttk.Label(top_frame, text="", font=("Helvetica", 12, "bold italic"),
                               image=self.logo, background= "#003455")
        main_label.pack(fill = "none", expand=True)
        # ---- info frame to indicate what option is selected
        info_frame = ttk.Frame(master, padding="1 1 1 1",style='Black.TLabelframe')
        info_frame.pack(side=TOP, fill="both")

        # ---- set canvas and info frame background
        self.tempimg = Image.open("./gif_images/background.gif")
        self.tempimg = self.tempimg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(image=self.tempimg)

        self.frmtempimg = Image.open("./gif_images/frame_backimg1.gif")

        self.frmtempimg = self.frmtempimg.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        self.frame_back_image = ImageTk.PhotoImage(image=self.frmtempimg)

        self.info_label_backgrnd = ttk.Label(info_frame, image=self.frame_back_image, border=0)
        self.info_label_backgrnd.pack(fill = BOTH, expand = True)

        self.info_label = ttk.Label(self.info_label_backgrnd, text="", textvariable=self.selected_info, font=("Times", 20, "bold"), anchor = CENTER, foreground="white", background = "#154360", border=0) #002366
        self.info_label.grid(column=1, row=0, sticky=( W, E)) #pack(fill = "none", expand = True, side = LEFT) #
        self.info_labelimg = ttk.Label(self.info_label_backgrnd, image=self.selected_info_image, border=0)
        self.info_labelimg.grid(column=2, row=0, sticky=(N, W, E, S)) #pack(fill="none",  side = LEFT)  # grid(column=1, row=0, sticky=(N, W, E, S))

        root.columnconfigure(3, weight=1)
        root.rowconfigure(0, weight=1)
        for child in self.info_label_backgrnd.winfo_children(): child.grid_configure(padx=10, pady=10)

        self.can = Canvas(self)
        self.can.pack(side=TOP, fill="both", expand=True)
        self.can.config(bd = 4, relief = "sunken")


        self.image_obj = self.can.create_image((self.tempimg.size[0] // 2), (self.tempimg.size[1] // 2),
                                               image=self.background_image, anchor=CENTER)

        self.set_item_mainscreen("meal")



        # ----  message_frame to show final  message
        message_frame = ttk.Frame(master, padding="15 15 15 15",  style='Black.TLabel')
        message_frame.pack(side=BOTTOM, fill="both")
        message_label = ttk.Label(message_frame, textvariable=self.requested_msg, foreground="white",background="#003455", font=("Times", 17, "bold"))
        message_label.pack(fill="none", expand=True)




if __name__ == "__main__":
    root = Tk()

    main = MainView(root)
    root.title("Health Talk")

    root.geometry('%dx%d' % (root.winfo_screenwidth() / 1.6, root.winfo_screenheight() / 1.2))

    root.update()  # to get actual geometry of root
    main.pack(side="top", fill="both", expand=True)
    root.after(2000, main.calculate)
    root.mainloop()

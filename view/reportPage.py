from tkinter import *
from tkinter.ttk import Combobox
import nibabel as nib
from static import style, config
from view.app import GUI
from models.images import Images
from models.registration import Registration

class Report(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.size_img = 0

        frame1 = LabelFrame(self, style.frame_styles, text="Seleccionar la imagen")
        frame1.place(rely=0.05, relx=0.02, height=150, width=400)

        self.frame2 = LabelFrame(self, style.frame_styles, text="Imagen original")
        self.frame2.place(rely=0.05, relx=0.45, height=600, width=550)
        
        self.frame3 = LabelFrame(self, style.frame_styles, text="Información general")
        self.frame3.place(rely=0.33, relx=0.02, height=350, width=400)

        label1 = Label(
            frame1,           
            text= "Selecciona una imagen médica",
            justify=CENTER, 
            **style.frame_styles
        )
        label1.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.combobox_imgs = Combobox(frame1, 
            font= style.FONT,
            state= 'readonly',
        )
        self.combobox_imgs.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=3)

        self.upload_img = PhotoImage(file=config.RESOURCES['icons'].format('add'),)
        img_button = Button(frame1,
            **style.frame_styles,
            image=self.upload_img,
        )
        img_button.pack(side=LEFT, padx=5, pady=3)

        label2 = Label(
            self.frame2,           
            text= "Vista",
            justify=CENTER, 
            **style.frame_styles
        )
        label2.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.combobox_views = Combobox(self.frame2,              
            font= style.FONT,
            state= 'readonly',
        )
        self.combobox_views.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)
        
        self.original_label = Label(
            self.frame2,           
            text= "Imagen original ",
            justify=CENTER, 
            **style.frame_styles,
        ).pack(side=TOP, fill=X, expand=True, padx=5, pady=3) 
        self.canvas = Canvas(self.frame2, bg='white', width=450, height=380)
        self.canvas.pack(side=TOP )

        #  slider
        current_value = IntVar()  
        self.slider = Scale(
            self.frame2,
            from_=0,
            to=100,
            bg='white',
            orient='horizontal',  # vertical
            variable=current_value
        )
        self.slider.pack(side=TOP, fill=X, expand=True, padx=5, pady=0)          

        call_methods = Images(self.combobox_views, self.combobox_imgs, self.slider, self.canvas)

        self.combobox_views['values']=call_methods.load_data_combobox("combobox_views")
        self.combobox_views.current(0)
        self.combobox_views.bind("<<ComboboxSelected>>", lambda event: call_methods.show_img(self.slider.get()))
        self.combobox_imgs['values'] =call_methods.load_data_combobox("combobox_imgs")
        self.combobox_imgs.current(0)
        self.combobox_imgs.bind("<<ComboboxSelected>>", lambda event: self.upload_data(call_methods))
        img_button['command'] = call_methods.load_image_button
        self.slider['command'] = call_methods.update_slide

    def upload_data(self, call):
        call.load_img()
        data=Registration.calculate_metrics(call.image, nib.load(config.RESOURCES['imgs'].format('seg_148.nii.gz')))
        data_volumen = Registration.calculate_volumes(call.image)
        call.update_info(self.frame3,"report", data, data_volumen)
        print(data)

    
from tkinter import *
from tkinter.ttk import Combobox
from static import style, config
from models import images, intensitiesStandarization
from view.app import GUI

class Rescaled(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)

        frame1 = LabelFrame(self, style.frame_styles, text="Imagen original")
        frame1.place(rely=0.05, relx=0.02, height=460, width=400)

        frame2 = LabelFrame(self, style.frame_styles, text="Estandarización de intensidades usando rescalado")
        frame2.place(rely=0.05, relx=0.45, height=600, width=550)
        
        frame3 = LabelFrame(self, style.frame_styles, text="Configuración de rescalado")
        frame3.place(rely=0.75, relx=0.02, height=140, width=400)

        label1 = Label(frame1, text= "Selecciona una imagen médica", justify=CENTER, **style.frame_styles)
        label1.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.combobox_imgs = Combobox(frame1, font= style.FONT, state= 'readonly')
        self.combobox_imgs.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)
        
        label2 = Label(frame1, text= "Vista", justify=CENTER, **style.frame_styles)
        label2.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.combobox_views = Combobox(frame1, font= style.FONT, state= 'readonly')
        self.combobox_views.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)
        
        self.canvas = Canvas(frame1, bg='white', width=300, height=230)
        self.canvas.pack(side=TOP )

        #  slider
        current_value = IntVar()  
        self.slider = Scale(frame1, from_=0, to=100, bg='white', orient='horizontal', variable=current_value)
        self.slider.pack(side=TOP, fill=X, expand=True, padx=5, pady=0)          

        label3 = Label(frame2, text= "Vista", justify=CENTER, **style.frame_styles)
        label3.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.combobox_views_seg = Combobox(frame2, font= style.FONT, state= 'readonly')
        self.combobox_views_seg.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)
        
        self.segmented_label = Label(frame2, text= "Imagen filtrada", justify=CENTER, **style.frame_styles,)
        self.segmented_label.pack(side=TOP, fill=X, expand=True, padx=5, pady=3) 
        self.canvas_segmented = Canvas(frame2, bg='white', width=450, height=380)
        self.canvas_segmented.pack(side=TOP )

        #  slider
        current_value_segmented = IntVar()  
        self.slider_segmented = Scale(frame2, from_=0, to=100, bg='white', orient='horizontal', variable=current_value_segmented)
        self.slider_segmented.pack(side=TOP, fill=X, expand=True, padx=5, pady=0)          


        self.upload_saved = PhotoImage(file=config.RESOURCES['icons'].format('saved'),)
        img_button = Button(frame2, **style.frame_styles, image=self.upload_saved)
        img_button.pack(side=LEFT, expand=True,  padx=5, pady=3)

        self.bt_segmentation = Button(frame3, **style.button_style, text="Estandarizar")
        self.bt_segmentation.pack(side=BOTTOM, expand=True, fill=X, padx=5, pady=3)

        
        call_methods = images.Images(self.combobox_views, self.combobox_imgs, self.slider, self.canvas)
        self.combobox_views['values']=call_methods.load_data_combobox("combobox_views")
        self.combobox_views.current(0)
        self.combobox_views.bind("<<ComboboxSelected>>", lambda event: call_methods.show_img(self.slider.get()))
        self.combobox_imgs['values'] =call_methods.load_data_combobox("combobox_imgs")
        self.combobox_imgs.current(0)
        self.combobox_imgs.bind("<<ComboboxSelected>>", lambda event: call_methods.load_img() )
        self.slider['command'] = call_methods.update_slide

        call_methods_seg = images.Images(self.combobox_views_seg, self.combobox_imgs, self.slider_segmented, self.canvas_segmented)
        self.combobox_views_seg['values']=call_methods_seg.load_data_combobox("combobox_views")
        self.combobox_views_seg.current(0)
        self.combobox_views_seg.bind("<<ComboboxSelected>>", lambda event: call_methods_seg.show_img(self.slider_segmented.get()))
        self.slider_segmented['command'] = call_methods_seg.update_slide
        self.bt_segmentation['command'] = lambda : (intensitiesStandarization.IntensitiesStandarization.rescaling(call_methods.mri_image, call_methods_seg), 
                                                    call_methods_seg.set_slider(), call_methods_seg.show_img(self.slider_segmented.get()))
        img_button['command'] = lambda : call_methods_seg.save_image("Rescaled")


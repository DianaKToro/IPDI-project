from tkinter import *
from tkinter.ttk import Combobox
from static import style, config
from models import segmentation, images 
from view.app import GUI

class Histograms(GUI):
    def __init__(self, parent, controller):
        GUI.__init__(self, parent)
        self.tau = IntVar()
        self.tol = IntVar()

        frame1 = LabelFrame(self, style.frame_styles, text="Histograma de imagen original")
        frame1.place(rely=0.05, relx=0.02, height=500, width=430)

        frame2 = LabelFrame(self, style.frame_styles, text="Histograma de imagen procesada")
        frame2.place(rely=0.05, relx=0.45, height=600, width=550)
        
        label1 = Label(frame1, text= "Selecciona una imagen médica", justify=CENTER, **style.frame_styles)
        label1.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.combobox_imgs = Combobox(frame1, font= style.FONT, state= 'readonly')
        self.combobox_imgs.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)    
        
        self.canvas = Canvas(frame1, bg='white', width=400, height=410)
        self.canvas.pack(side=TOP )
        
        self.combobox_views = Combobox(frame1, font= style.FONT, state= 'readonly')
        self.combobox_views.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)

        #  slider
        current_value = IntVar()  
        self.slider = Scale(frame1, from_=0, to=100, bg='white', orient='horizontal', variable=current_value)
        self.slider.pack(side=TOP, fill=X, expand=True, padx=5, pady=0) 
        
        label1 = Label(frame2, text= "Selecciona una imagen médica", justify=CENTER, **style.frame_styles)
        label1.pack(side=TOP, fill=X, expand=True, padx=5, pady=3)  

        self.second_combobox_imgs = Combobox(frame2, font= style.FONT, state= 'readonly')
        self.second_combobox_imgs.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)      
        
        self.canvas_segmented = Canvas(frame2, bg='white', width=500, height=510)
        self.canvas_segmented.pack(side=TOP )

        self.combobox_views_seg = Combobox(frame2, font= style.FONT, state= 'readonly')
        self.combobox_views_seg.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=3)

        #  slider
        current_value_segmented = IntVar()  
        self.slider_segmented = Scale(frame2, from_=0, to=100, bg='white', orient='horizontal', variable=current_value_segmented)
        self.slider_segmented.pack(side=TOP, fill=X, expand=True, padx=5, pady=0)          

        call_methods = images.Images(self.combobox_views, self.combobox_imgs, self.slider, self.canvas)
        self.combobox_views['values']=call_methods.load_data_combobox("combobox_views")
        self.combobox_views.current(0)
        self.combobox_views.bind("<<ComboboxSelected>>", lambda event: call_methods.show_img(self.slider.get()))
        self.combobox_imgs['values'] =call_methods.load_data_combobox("combobox_imgs")
        self.combobox_imgs.current(0)
        self.combobox_imgs.bind("<<ComboboxSelected>>", lambda event: call_methods.show_histogram() )

        call_methods_seg = images.Images(self.combobox_views_seg, self.second_combobox_imgs, self.slider_segmented, self.canvas_segmented)
        self.combobox_views_seg['values']=call_methods_seg.load_data_combobox("combobox_views")
        self.combobox_views_seg.current(0)
        self.combobox_views_seg.bind("<<ComboboxSelected>>", lambda event: call_methods_seg.show_img(self.slider_segmented.get()))
        self.second_combobox_imgs['values'] =call_methods.load_data_combobox("combobox_imgs")
        self.second_combobox_imgs.current(0)
        self.second_combobox_imgs.bind("<<ComboboxSelected>>", lambda event: call_methods_seg.show_histogram() )



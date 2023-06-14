import os
import nibabel as nib
import numpy as np
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from static import style, config
import matplotlib.pyplot as plt
import ants
from tkinter import *
from tkinter import messagebox

class Images:
    def __init__(self, combobox_view=None, combobox_img = None, slider = None, canvas = None):
        self.view = combobox_view
        self.name_img = combobox_img
        self.slider = slider
        self.canvas = canvas
        self.image = None

    def load_data_combobox(self, combobox):
        data = []

        if combobox == "combobox_imgs":
            files = sorted(os.listdir("resources/imgs/"), key=len)

            for file in files:
                f = file.split('.')
                
                if f[1] == "nii":
                    f = file.split('.')
                    if f[2] == "gz":
                        data.append(f[0] + "."+ f[1]+ "."+ f[2])

        elif combobox == "combobox_views":
            for (key, value) in config.VIEWS.items():
                data.append(key + value)        
        
        return data
    
    def load_image_button(self,):
        """Select an image to display"""
        filename = filedialog.askopenfilename()        
        image = nib.load(filename)
        old_route = config.RESOURCES['imgs'].split('/')
        route_old_img = old_route[-3] + "/"+ old_route[-2]+ "/"
        split_filename = filename.split('/')
        name_img = split_filename[-1]
        route_new_img = split_filename[-3] + "/"+ split_filename[-2]+ "/"
        route = route_old_img + name_img
        
        if route_old_img != route_new_img:          
            nib.save(image, route)  
        
        self.name_img.set(name_img)  
        self.load_img()  
               
    def load_img(self):
        name_img = self.name_img.get()
        self.image = nib.load(config.RESOURCES['imgs'].format(name_img))      
        self.mri_image = self.image.get_fdata() 
        self.set_slider()
        self.show_img(40)

    def set_slider(self):        
        size_img = self.get_size_slide()          
        self.slider.configure(to=size_img)
        
      
    def get_size_slide(self):
        if self.view.get() == "Sagital Y":
            size_img = (self.mri_image.shape[1])-1           
        if self.view.get() == "Coronal Z":
            size_img = (self.mri_image.shape[2])-1            
        else:    
            size_img = (self.mri_image.shape[0])-1            
        return size_img
        
    def update_slide(self, var):
        self.show_img(self.slider.get())

    def show_img(self, value_slide, ):
        self.canvas.delete("all")
        url_img = self.name_img.get()
        split_url = url_img.split('_')
        type_mri = split_url[1].split('.')
        
        fig, axs = plt.subplots()
        if self.view.get() == "Coronal X": 
            image = self.mri_image[value_slide, :, :]
            if type_mri[0] == "IR":
                image = self.mri_image[:, value_slide, :]
                axs.imshow(image.T, origin="lower", cmap='gray')
            elif type_mri[0] == "FLAIR":
                image = self.mri_image[:, value_slide, :]
                axs.imshow(image.T, origin="lower", cmap='gray')
            else:
                axs.imshow(image, cmap='gray')
        elif self.view.get() == "Sagital Y":
            image = self.mri_image[:, :, value_slide].T                        
            if type_mri[0] == "IR":                
                image = self.mri_image[value_slide, : , :] 
                axs.imshow(image.T, origin="lower", cmap='gray')
            elif type_mri[0] == "FLAIR":
                image = self.mri_image[value_slide, : , :] 
                axs.imshow(image.T, origin="lower", cmap='gray')           
            else:
                axs.imshow(image, cmap='gray')
        elif self.view.get() == "Axial Z":
            image =self.mri_image[:, value_slide, :] 
            if type_mri[0] == "IR":                
                image = self.mri_image[:, :, value_slide] 
                axs.imshow(image.T , cmap='gray')
            elif type_mri[0] == "FLAIR":                
                image = self.mri_image[:, :, value_slide] 
                axs.imshow(image.T, cmap='gray')    
            else:
                axs.imshow(image, cmap='gray')    
        
        plt.axis('off')                        
        plt.close()
        
        self.original_label = FigureCanvasTkAgg(fig, self.canvas)
        self.original_label.draw()
        self.original_label.get_tk_widget().place(x=0, y=0, height=int(self.canvas.winfo_reqheight()), width=int(self.canvas.winfo_reqwidth()))
    
    def save_image(self, type_img):
        """Save image to a file"""        
        name_img = self.name_img.get()
        image = nib.load(config.RESOURCES['imgs'].format(name_img))
        nifti_imgs = nib.Nifti1Image(self.mri_image, image.affine, image.header)
        filename = config.RESOURCES['imgs'].format(type_img + "_" +self.name_img.get())
        nib.save(nifti_imgs, filename)
        messagebox.showinfo("Proceso exitoso", "Se ha guardado correctamente la imagen")
        self.name_img.set(type_img + "_" +name_img)  

    
    def save_image_registration(self, type_img):
        """Save image to a file"""        
        name_img = self.name_img.get()
        filename = config.RESOURCES['imgs'].format(type_img + "_" +self.name_img.get())
        ants.image_write(self.mri_image, filename, ri=True)
        messagebox.showinfo("Proceso exitoso", "Se ha guardado correctamente la imagen")
        self.name_img.set(type_img + "_" +name_img) 

        
    def update_info(self, frame, view_menu, data_metrics=None, data_volumen = None):
        if view_menu == "images":
            self.clear_frame(frame)
            info_axis_x = "El tamaño de la MRI en el eje X es: " + str(self.mri_image.shape[0])        
            info_axis_y = "El tamaño de la MRI en el eje Y es: " + str(self.mri_image.shape[1])        
            info_axis_z = "El tamaño de la MRI en el eje Z es: " + str(self.mri_image.shape[2])        
            info_intensity_min = "El valor mínimo de la intensidad del vóxel es: " + str(int(np.min(self.mri_image)))
            info_intensity_max = "El valor máximo de la intensidad del vóxel es: " + str(int(np.max(self.mri_image))) 
            label_axis_x = Label(frame, text=info_axis_x, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW)         
            label_axis_y = Label(frame, text=info_axis_y, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW)        
            label_axis_z = Label(frame, text=info_axis_z, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW)    
            label_intensity_min = Label(frame, text=info_intensity_min, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW)    
            label_intensity_max = Label(frame, text=info_intensity_max, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW)    
        
        if view_menu == "report":
            self.clear_frame(frame)
            for (key, value) in data_metrics.items():
                
                info_axis_x = "La compaaración de las segmentaciones "+ key + " son: " + str(value)             
                Label(frame, text=info_axis_x, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW) 
            for (key, value) in data_volumen.items():
                
                info_axis_x = "El volumen del label "+ str(key) + " es: " + str(value)             
                Label(frame, text=info_axis_x, font=style.FONT, bg=style.BG, fg=style.FG).pack(side=TOP, anchor=NW) 
            

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy() 
    
    def show_histogram(self):
        name_img = self.name_img.get()
        image = nib.load(config.RESOURCES['imgs'].format(name_img))      
        self.mri_image = image.get_fdata()
        fig, axs = plt.subplots() 

        axs.hist(self.mri_image.flatten(), 100, alpha=0.5)
        plt.close()
        
        self.original_label = FigureCanvasTkAgg(fig, self.canvas)
        self.original_label.draw()
        self.original_label.get_tk_widget().place(x=0, y=0, height=int(self.canvas.winfo_reqheight()), width=int(self.canvas.winfo_reqwidth()))
    
        
     
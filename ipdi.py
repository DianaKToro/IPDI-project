from controller.manager import Manager

class IpdiApp:
    def main(self):
        app = Manager()
        app.mainloop()

if __name__ == "__main__":
    IpdiApp().main()
import cv2
import ast
import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Escáner de Kits")
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Escaneando QR...", font=("Arial", 16))
        self.label.pack()

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.button = tk.Button(root, text="Sacar del almacén", command=self.sacar_del_almacen, state="disabled")
        self.button.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()

        self.item_actual = None  # para guardar temporalmente el kit leído

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            data, bbox, _ = self.detector.detectAndDecode(frame)
            if data:
                try:
                    item = ast.literal_eval(data)
                    self.item_actual = item
                    self.verificar_en_mysql(item)

                    if bbox is not None:
                        for i in range(len(bbox)):
                            pt1 = tuple(map(int, bbox[i][0]))
                            pt2 = tuple(map(int, bbox[(i + 1) % len(bbox)][0]))
                            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo procesar el QR\n{e}")

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.imgtk = imgtk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

        self.root.after(10, self.update_frame)

    def verificar_en_mysql(self, item):
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="********",
                database="ultrasteeldata",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM almacen WHERE id = %s", (item['id'],))
            resultado = cursor.fetchone()

            if resultado:
                self.label.config(text=f"✅ El Kit {item['id']} se encuentra registrado")
                print(f"El Kit {item['id']} se encuentra registrado")
                self.button.config(state="normal")
            else:
                self.label.config(text="⚠️ Kit NO registrado")
                self.button.config(state="disabled")

            cursor.close()
            conexion.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error MySQL", str(e))

    def sacar_del_almacen(self):
        if not self.item_actual:
            return

        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="********",
                database="ultrasteeldata",
                port=3306
            )
            cursor = conexion.cursor()
            cursor.execute("UPDATE almacen SET estatus = %s WHERE id = %s", ("Salió del almacén", self.item_actual['id']))
            conexion.commit()

            messagebox.showinfo("Actualizado", "Estatus actualizado a 'Salió del almacén'")
            self.label.config(text="📦 Estatus actualizado")
            self.button.config(state="disabled")

            cursor.close()
            conexion.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Error al actualizar", str(e))

    def on_closing(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

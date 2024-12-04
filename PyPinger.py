import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, scrolledtext
from ping3 import ping
import datetime
import threading
import time

class ScrolledFrame(ttk.Frame):
    """A frame that can be scrolled."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create a canvas for scrolling
        self.canvas = ttk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure the canvas
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Configure canvas to work with scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

class PingApp:
    def __init__(self, master):
        self.master = master
        master.title("IP Ping Logger")

        self.ip_list = []
        self.ip_dict = {}
        self.is_pinging = False
        self.ping_threads = {}

        # Frame for IP address and Identifier input
        input_frame = ttk.Frame(master)
        input_frame.pack(pady=10)

        # Input for IP address
        self.ip_label = ttk.Label(input_frame, text="IP Address:")
        self.ip_label.grid(row=0, column=0)

        self.ip_entry = ttk.Entry(input_frame)
        self.ip_entry.grid(row=0, column=1, padx=5)

        # Input for Identifier
        self.id_label = ttk.Label(input_frame, text="Identifier:")
        self.id_label.grid(row=0, column=2)

        self.id_entry = ttk.Entry(input_frame)
        self.id_entry.grid(row=0, column=3, padx=5)

        # Save button with ttkbootstrap styling
        self.save_button = ttk.Button(input_frame, text="Save IP", bootstyle="success-outline", command=self.save_ip)
        self.save_button.grid(row=0, column=4, padx=5)

        # Frame for Removing IP
        remove_frame = ttk.Frame(master)
        remove_frame.pack(pady=10)

        # Input for Removing IP
        self.remove_label = ttk.Label(remove_frame, text="Remove IP Address:")
        self.remove_label.grid(row=0, column=0)

        self.remove_entry = ttk.Entry(remove_frame)
        self.remove_entry.grid(row=0, column=1, padx=5)

        # Remove button with ttkbootstrap styling
        self.remove_button = ttk.Button(remove_frame, text="Remove IP", bootstyle="danger-outline", command=self.remove_ip)
        self.remove_button.grid(row=0, column=2, padx=5)

        # Frame for Start/Stop buttons
        control_frame = ttk.Frame(master)
        control_frame.pack(pady=10)

        # Start Continuous Ping Button
        self.ping_button = ttk.Button(control_frame, text="Start Continuous Ping", bootstyle="primary", command=self.start_continuous_ping)
        self.ping_button.grid(row=0, column=0, padx=5)

        # Stop Continuous Ping Button
        self.stop_button = ttk.Button(control_frame, text="Stop Continuous Ping", bootstyle="danger", command=self.stop_continuous_ping)
        self.stop_button.grid(row=0, column=1, padx=5)

        # Create a scrollable frame for log output
        self.log_frame = ScrolledFrame(master)
        self.log_frame.pack(fill=ttk.BOTH, expand=True)

        # Load saved IPs
        self.load_ips()

    def save_ip(self):
        ip = self.ip_entry.get()
        identifier = self.id_entry.get()
        
        if not ip or not identifier:
            messagebox.showwarning("Warning", "Please enter a valid IP address and identifier.")
            return

        # Check for duplicate IP
        if ip in self.ip_list:
            messagebox.showwarning("Warning", f"IP address {ip} already exists.")
            return

        self.ip_list.append(ip)
        self.ip_dict[ip] = identifier
        with open("ips.txt", "a") as file:
            file.write(f"{ip},{identifier}\n")
        self.ip_entry.delete(0, ttk.END)
        self.id_entry.delete(0, ttk.END)
        messagebox.showinfo("Info", f"IP {ip} with identifier '{identifier}' saved.")
        self.start_continuous_ping()  # Automatically start pinging the new IP

    def continuous_ping(self, ip, identifier):
        # Create a new frame for the specific IP and identifier
        entry_frame = ttk.Frame(self.log_frame.scrollable_frame)
        entry_frame.pack(pady=5, fill=ttk.X)

        # Create and pack the identifier label above the ScrolledText
        id_label = ttk.Label(entry_frame, text=f"{identifier}:", font=("Helvetica", 12, "bold"), anchor="w")
        id_label.pack(anchor="w")

        # Create a new ScrolledText for the specific IP
        log_area = scrolledtext.ScrolledText(entry_frame, wrap=ttk.WORD, height=5, width=90, bg='black', fg='white')
        log_area.pack(fill=ttk.X, expand=True)

        # Start pinging in a new thread
        self.ping_threads[ip] = log_area  # Keep reference to the log area
        threading.Thread(target=self.ping_ip, args=(ip, log_area), daemon=True).start()

    def ping_ip(self, ip, log_area):
        while self.is_pinging and ip in self.ip_list:
            response = ping(ip)
            timestamp = datetime.datetime.now().strftime('%a %m/%d/%Y %I:%M:%S %p')

            if response is not None:
                log_message = f"{timestamp} - Reply from {ip}: bytes=32 time={response * 1000:.2f}ms TTL=58"
            else:
                log_message = f"{timestamp} - Reply from {ip}: Request timed out."

            self.insert_log(log_area, log_message, ip)
            time.sleep(2)


    def insert_log(self, log_area, log_message, ip):
        # Insert log into the GUI
        log_area.insert(ttk.END, log_message + "\n")
        log_area.see(ttk.END)

        # Generate a folder and filename based on the current date
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        log_folder = date_str
        os.makedirs(log_folder, exist_ok=True)
        filename = os.path.join(log_folder, f"{ip}_log.txt")

        # Save log to the daily file within the dated folder
        with open(filename, "a") as file:
            file.write(log_message + "\n")

    def start_continuous_ping(self):
        if not self.is_pinging:
            self.is_pinging = True
            for ip in self.ip_list:
                identifier = self.ip_dict[ip]
                if ip not in self.ping_threads:
                    self.continuous_ping(ip, identifier)

    def stop_continuous_ping(self):
        self.is_pinging = False
        self.ping_threads.clear()  # Clear threads so they can restart if needed
        messagebox.showinfo("Info", "Continuous pinging stopped.")

    def remove_ip(self):
        ip_to_remove = self.remove_entry.get()
        if ip_to_remove in self.ip_list:
            self.ip_list.remove(ip_to_remove)
            del self.ip_dict[ip_to_remove]

            # Stop the corresponding thread if it's still running
            self.is_pinging = False
            if ip_to_remove in self.ping_threads:
                log_area = self.ping_threads[ip_to_remove]
                log_area.master.destroy()  # Remove its log area
                del self.ping_threads[ip_to_remove]

            # Update the file
            with open("ips.txt", "w") as file:
                for ip, identifier in self.ip_dict.items():
                    file.write(f"{ip},{identifier}\n")

            self.remove_entry.delete(0, ttk.END)
            messagebox.showinfo("Info", f"IP {ip_to_remove} removed successfully.")
        else:
            messagebox.showwarning("Warning", "IP address not found.")

    def load_ips(self):
        try:
            with open("ips.txt", "r") as file:
                for line in file:
                    ip, identifier = line.strip().split(",")
                    self.ip_list.append(ip)
                    self.ip_dict[ip] = identifier
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  # Using a modern dark theme
    app = PingApp(root)
    root.mainloop()

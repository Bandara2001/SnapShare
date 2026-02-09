# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from utils import discover_devices, start_response_listener
from client import send_file
import threading

# Start listener to respond to discovery messages
start_response_listener()

# Modern color palette
COLORS = {
    'bg_primary': '#0F172A',      # Dark slate
    'bg_secondary': '#1E293B',    # Lighter slate
    'accent': '#3B82F6',          # Blue
    'accent_hover': '#2563EB',    # Darker blue
    'success': '#10B981',         # Green
    'text_primary': '#F1F5F9',    # Light text
    'text_secondary': '#94A3B8',  # Gray text
    'border': '#334155'           # Border color
}

root = tk.Tk()
root.title("SnapShare")
root.geometry("500x650")
root.configure(bg=COLORS['bg_primary'])
root.resizable(False, False)

# Custom style
style = ttk.Style()
style.theme_use('clam')

# Configure ttk styles
style.configure('Custom.TButton',
                background=COLORS['accent'],
                foreground=COLORS['text_primary'],
                borderwidth=0,
                focuscolor='none',
                font=('Segoe UI', 10, 'bold'),
                padding=12)
style.map('Custom.TButton',
          background=[('active', COLORS['accent_hover'])])

# Header Frame
header_frame = tk.Frame(root, bg=COLORS['bg_primary'], pady=20)
header_frame.pack(fill='x')

# App Title with icon effect
title_label = tk.Label(header_frame, 
                       text="⚡ SnapShare", 
                       font=('Segoe UI', 28, 'bold'),
                       bg=COLORS['bg_primary'],
                       fg=COLORS['text_primary'])
title_label.pack()

subtitle_label = tk.Label(header_frame, 
                         text="Fast & Secure File Sharing", 
                         font=('Segoe UI', 11),
                         bg=COLORS['bg_primary'],
                         fg=COLORS['text_secondary'])
subtitle_label.pack()

# Main container
main_container = tk.Frame(root, bg=COLORS['bg_primary'], padx=30)
main_container.pack(fill='both', expand=True)

# Devices Section
devices_label = tk.Label(main_container, 
                        text="📱 Available Devices", 
                        font=('Segoe UI', 14, 'bold'),
                        bg=COLORS['bg_primary'],
                        fg=COLORS['text_primary'],
                        anchor='w')
devices_label.pack(fill='x', pady=(0, 10))

# Device list frame with border
device_frame = tk.Frame(main_container, 
                       bg=COLORS['border'], 
                       padx=1, 
                       pady=1)
device_frame.pack(fill='both', expand=True, pady=(0, 15))

# Scrollbar
scrollbar = tk.Scrollbar(device_frame, bg=COLORS['bg_secondary'])
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Device listbox with modern styling
device_list = tk.Listbox(device_frame,
                        width=40,
                        height=8,
                        bg=COLORS['bg_secondary'],
                        fg=COLORS['text_primary'],
                        selectbackground=COLORS['accent'],
                        selectforeground=COLORS['text_primary'],
                        font=('Segoe UI', 11),
                        borderwidth=0,
                        highlightthickness=0,
                        activestyle='none',
                        yscrollcommand=scrollbar.set)
device_list.pack(side=tk.LEFT, fill='both', expand=True, padx=1, pady=1)
scrollbar.config(command=device_list.yview)

filepath_var = tk.StringVar()

# Custom Button Class for modern look
class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, icon="", bg_color=COLORS['accent'], **kwargs):
        super().__init__(parent, height=50, bg=COLORS['bg_primary'], 
                        highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = COLORS['accent_hover'] if bg_color == COLORS['accent'] else COLORS['success']
        self.text = text
        self.icon = icon
        
        self.rect = self.create_rectangle(0, 0, 440, 50, 
                                          fill=self.bg_color, 
                                          outline="",
                                          tags="button")
        self.text_item = self.create_text(220, 25, 
                                         text=f"{self.icon} {self.text}", 
                                         fill=COLORS['text_primary'],
                                         font=('Segoe UI', 11, 'bold'),
                                         tags="button")
        
        self.tag_bind("button", "<Enter>", self.on_enter)
        self.tag_bind("button", "<Leave>", self.on_leave)
        self.tag_bind("button", "<Button-1>", self.on_click)
        
    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor="")
        
    def on_click(self, event):
        self.command()

# Refresh devices function
def refresh_devices():
    device_list.delete(0, tk.END)
    # Add loading indicator
    device_list.insert(tk.END, "🔄 Searching for devices...")
    device_list.itemconfig(0, {'fg': COLORS['text_secondary']})
    root.update()
    
    devices = discover_devices()
    device_list.delete(0, tk.END)
    
    if devices:
        for d in devices:
            device_list.insert(tk.END, f"  🖥️  {d}")
    else:
        device_list.insert(tk.END, "  No devices found")
        device_list.itemconfig(0, {'fg': COLORS['text_secondary']})

# Refresh button
refresh_btn = ModernButton(main_container, 
                          "Refresh Devices", 
                          lambda: threading.Thread(target=refresh_devices, daemon=True).start(),
                          icon="🔄")
refresh_btn.pack(pady=(0, 20))

# File selection section
file_label = tk.Label(main_container, 
                     text="📄 File Selection", 
                     font=('Segoe UI', 14, 'bold'),
                     bg=COLORS['bg_primary'],
                     fg=COLORS['text_primary'],
                     anchor='w')
file_label.pack(fill='x', pady=(0, 10))

# Selected file display
selected_file_frame = tk.Frame(main_container, 
                              bg=COLORS['bg_secondary'], 
                              height=50)
selected_file_frame.pack(fill='x', pady=(0, 15))
selected_file_frame.pack_propagate(False)

selected_file_label = tk.Label(selected_file_frame, 
                              text="No file selected", 
                              font=('Segoe UI', 10),
                              bg=COLORS['bg_secondary'],
                              fg=COLORS['text_secondary'],
                              anchor='w',
                              padx=15)
selected_file_label.pack(fill='both', expand=True)

# Browse file function
def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        filepath_var.set(filepath)
        # Show just the filename for better UX
        filename = filepath.split('/')[-1]
        selected_file_label.config(text=f"✓ {filename}", 
                                  fg=COLORS['success'])
        messagebox.showinfo("File Selected", f"Selected: {filename}")

# Browse button
browse_btn = ModernButton(main_container, 
                         "Browse File", 
                         browse_file,
                         icon="📁")
browse_btn.pack(pady=(0, 15))

# Send selected file function
def send_selected_file():
    selected = device_list.curselection()
    if not selected:
        messagebox.showwarning("No Device", "Please select a device to send the file to.")
        return
    if not filepath_var.get():
        messagebox.showwarning("No File", "Please select a file to send.")
        return
    
    # Get the device IP (remove emoji and spaces)
    device_text = device_list.get(selected[0])
    ip = device_text.replace("🖥️", "").strip()
    
    # Update button text during send
    selected_file_label.config(text="📤 Sending file...", 
                              fg=COLORS['accent'])
    
    def send_and_notify():
        send_file(ip, filepath_var.get())
        root.after(0, lambda: selected_file_label.config(
            text=f"✓ {filepath_var.get().split('/')[-1]}", 
            fg=COLORS['success']))
    
    threading.Thread(target=send_and_notify, daemon=True).start()

# Send button with success color
send_btn = ModernButton(main_container, 
                       "Send File", 
                       send_selected_file,
                       icon="📤",
                       bg_color=COLORS['success'])
send_btn.pack(pady=(0, 20))

# Footer
footer_label = tk.Label(root, 
                       text="Secure P2P File Transfer", 
                       font=('Segoe UI', 9),
                       bg=COLORS['bg_primary'],
                       fg=COLORS['text_secondary'])
footer_label.pack(pady=(0, 15))

root.mainloop()
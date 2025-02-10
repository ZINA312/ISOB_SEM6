import tkinter as tk
from tkinter import filedialog, messagebox

def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text: str, key: str) -> str:
    key = key.upper()
    key_index = 0
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            shifted = (ord(char) - base + key_shift) % 26
            result.append(chr(base + shifted))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def vigenere_decrypt(text: str, key: str) -> str:
    key = key.upper()
    key_index = 0
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_shift = ord(key[key_index % len(key)]) - ord('A')
            shifted = (ord(char) - base - key_shift) % 26
            result.append(chr(base + shifted))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def process_file():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    method = method_var.get()
    mode = mode_var.get()
    key = key_entry.get()

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if method == 'caesar':
            try:
                shift = int(key)
            except ValueError:
                messagebox.showerror("Ошибка", "Ключ для шифра Цезаря должен быть целым числом.")
                return
            if mode == 'encrypt':
                processed = caesar_encrypt(text, shift)
            else:
                processed = caesar_decrypt(text, shift)
        elif method == 'vigenere':
            if not key.isalpha():
                messagebox.showerror("Ошибка", "Ключ для шифра Виженера должен содержать только буквы.")
                return
            if mode == 'encrypt':
                processed = vigenere_encrypt(text, key)
            else:
                processed = vigenere_decrypt(text, key)
        else:
            messagebox.showerror("Ошибка", "Неизвестный метод шифрования.")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed)
        messagebox.showinfo("Успех", f"Файл успешно обработан. Результат сохранен в {output_file}")
    
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Входной файл не найден.")

def browse_input_file():
    filename = filedialog.askopenfilename()
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename()
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, filename)

app = tk.Tk()
app.title("Шифрование и дешифрование файлов")

tk.Label(app, text="Входной файл:").grid(row=0, column=0, padx=5, pady=5)
input_file_entry = tk.Entry(app, width=50)
input_file_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(app, text="Обзор", command=browse_input_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(app, text="Выходной файл:").grid(row=1, column=0, padx=5, pady=5)
output_file_entry = tk.Entry(app, width=50)
output_file_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(app, text="Обзор", command=browse_output_file).grid(row=1, column=2, padx=5, pady=5)

tk.Label(app, text="Метод:").grid(row=2, column=0, padx=5, pady=5)
method_var = tk.StringVar(value="caesar")
tk.Radiobutton(app, text="Цезарь", variable=method_var, value="caesar").grid(row=2, column=1, sticky=tk.W)
tk.Radiobutton(app, text="Виженер", variable=method_var, value="vigenere").grid(row=2, column=2, sticky=tk.W)

tk.Label(app, text="Режим:").grid(row=3, column=0, padx=5, pady=5)
mode_var = tk.StringVar(value="encrypt")
tk.Radiobutton(app, text="Шифрование", variable=mode_var, value="encrypt").grid(row=3, column=1, sticky=tk.W)
tk.Radiobutton(app, text="Дешифрование", variable=mode_var, value="decrypt").grid(row=3, column=2, sticky=tk.W)

tk.Label(app, text="Ключ:").grid(row=4, column=0, padx=5, pady=5)
key_entry = tk.Entry(app, width=50)
key_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Button(app, text="Обработать", command=process_file).grid(row=5, column=1, pady=10)

app.mainloop()
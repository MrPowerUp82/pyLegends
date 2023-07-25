import re, os
import datetime as dt
import tkinter as tk
import tkinter.filedialog as filedialog
from functools import partial
print("Selecione o binário (.exe) do Magick")
os.environ['IMAGEMAGICK_BINARY'] = filedialog.askopenfilename(filetypes=(("Magick of binary", "magick.exe"),))
from moviepy import editor

global music_name
global root
global entry
global label
global font_value
music_name = None
root = None
entry = None
label = None
font_value = 28

def on_enter_pressed(event, var_name):
    global root
    global entry
    exec(f"global {var_name}\n{var_name} = entry.get()")
    root.destroy()
    root.quit()

def mount_tk_entry(label_text, var_name):
    global root
    global entry
    global label
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 250
    window_height = 100
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    label = tk.Label(root, text=label_text)
    label.pack(side="left")
    entry = tk.Entry(root, bd=1)
    entry.bind('<Return>', partial(on_enter_pressed, var_name=var_name))
    entry.config(fg = 'black')
    entry.pack(side="left")
    root.mainloop()

print("Selecione o arquivo de legenda")
legend_file = filedialog.askopenfilename(filetypes=(("Arquivos de legenda", "*.srt"),))
print("Selecione o arquivo de video")
video_file = filedialog.askopenfilename(filetypes=(("Arquivos de video", "*.mp4"),))
print("Selecione o arquivo de audio (musica original)")
audio_file = filedialog.askopenfilename(filetypes=(("Arquivos de audio", "*.mp3"),))
legend = open(legend_file, 'r', encoding='utf-8').read()
pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n'
matches = re.findall(pattern, legend, re.DOTALL)
video = editor.VideoFileClip(video_file)
audio = editor.AudioFileClip(audio_file)
result_clips = []
result_clips.append(video)
print("Informe o nome da Música.")
mount_tk_entry("Music name: ", "music_name")
print("Informe o tamanho fonte.")
mount_tk_entry("Font value: ", "font_value")
for idx, match in enumerate(matches):
    index = match[0]
    time_range = match[1]
    phrase = match[2].strip()
    start_time_str, end_time_str = time_range.split(" --> ")
    start_time = dt.datetime.strptime(start_time_str, "%H:%M:%S,%f").time()
    end_time = dt.datetime.strptime(end_time_str, "%H:%M:%S,%f").time()
    if idx == 0 and music_name is not None:
        txt_clip = (editor.TextClip(music_name, fontsize=float(font_value), color='white', font='Open Sans')
        .set_start(0)
        .set_end(start_time.second+start_time.minute*60+start_time.microsecond/1e6)
        .set_position(('center', 'bottom')))
        result_clips.append(txt_clip)
    txt_clip = (editor.TextClip(phrase, fontsize=float(font_value), color='white', font='Open Sans')
    .set_start(start_time.second+start_time.minute*60+start_time.microsecond/1e6)
    .set_end(end_time.second+end_time.minute*60+end_time.microsecond/1e6)
    .set_position(('center', 'bottom')))
    result_clips.append(txt_clip)

result = editor.CompositeVideoClip(result_clips)
result = result.without_audio().set_audio(audio)
print("Selecione a pasta para salvar o arquivo de video")
output_dir = filedialog.askdirectory()
result = result.subclip(0, video.duration)
result.write_videofile(f"{output_dir}/video_final.mp4", codec="libx264", fps=30)

#input('Press any key to exit!')

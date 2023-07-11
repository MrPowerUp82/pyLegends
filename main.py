import re, os
import datetime as dt
import tkinter 
import tkinter.filedialog as filedialog
os.environ['IMAGEMAGICK_BINARY'] = filedialog.askopenfilename(filetypes=(("Magick of binary", "magick.exe"),))
from moviepy import editor

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
for match in matches:
    index = match[0]
    time_range = match[1]
    phrase = match[2].strip()
    start_time_str, end_time_str = time_range.split(" --> ")
    start_time = dt.datetime.strptime(start_time_str, "%H:%M:%S,%f").time()
    end_time = dt.datetime.strptime(end_time_str, "%H:%M:%S,%f").time()
    txt_clip = (editor.TextClip(phrase, fontsize=24, color='white', font='Open Sans')
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

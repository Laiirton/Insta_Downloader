import sys
import os
import re
import instaloader
from instaloader.exceptions import InvalidArgumentException
import time
import shutil
import concurrent.futures
import moviepy.editor as mp
import requests

def extract_shortcode(url):
    # Padrão para extrair o shortcode da URL
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/(?:p|reel|tv)\/([^\/?]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("URL inválida do Instagram")

def download_video(url, save_path, format):
    L = instaloader.Instaloader(dirname_pattern=save_path,
                                download_video_thumbnails=False,
                                download_geotags=False,
                                download_comments=False,
                                save_metadata=False,
                                compress_json=False,
                                download_pictures=False,  # Evita o download de imagens
                                post_metadata_txt_pattern='')  # Evita a criação do arquivo de texto
    
    try:
        shortcode = extract_shortcode(url)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if not post.is_video:
            return "Este post não contém um vídeo."
        
        # Baixar o vídeo manualmente
        video_url = post.video_url
        filename = f"{post.owner_username}_{post.date_utc:%Y-%m-%d_%H-%M-%S}.mp4"
        filepath = os.path.join(save_path, filename)
        
        response = requests.get(video_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        downloaded_size = 0
        
        with open(filepath, 'wb') as file:
            for data in response.iter_content(block_size):
                size = file.write(data)
                downloaded_size += size
                progress = int((downloaded_size / total_size) * 100)
                print(f"PROGRESS:{progress}", flush=True)
        
        if format == 'audio':
            # Converter para áudio
            audio_path = os.path.join(save_path, f"{post.owner_username}.mp3")
            video = mp.VideoFileClip(filepath)
            video.audio.write_audiofile(audio_path)
            video.close()
            os.remove(filepath)
            new_filename = f"{post.owner_username}.mp3"
        else:
            # Manter como vídeo
            new_filename = f"{post.owner_username}.mp4"
            new_path = os.path.join(save_path, new_filename)
            os.rename(filepath, new_path)
        
        # Remover outros arquivos
        for file in os.listdir(save_path):
            if file != new_filename:
                try:
                    os.remove(os.path.join(save_path, file))
                except PermissionError:
                    pass
        
        return f"{'Áudio' if format == 'audio' else 'Vídeo'} baixado com sucesso: {new_filename}"
    except ValueError as ve:
        return f"Erro: {str(ve)}"
    except InvalidArgumentException:
        return "Erro: Post não encontrado ou privado."
    except Exception as e:
        return f"Erro ao baixar o {'áudio' if format == 'audio' else 'vídeo'}: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python downloader.py <url> <save_path> <format>")
        sys.exit(1)
    
    url = sys.argv[1]
    save_path = sys.argv[2]
    format = sys.argv[3]
    result = download_video(url, save_path, format)
    print(result)  # Isso imprimirá apenas a mensagem de sucesso ou erro



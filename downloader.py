#!/usr/bin/env python

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

def generate_unique_filename(save_path, base_filename, extension):
    counter = 1
    new_filename = f"{base_filename}.{extension}"
    while os.path.exists(os.path.join(save_path, new_filename)):
        new_filename = f"{base_filename}_{counter}.{extension}"
        counter += 1
    return new_filename

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
        base_filename = f"{post.owner_username}_{post.date_utc:%Y-%m-%d_%H-%M-%S}"
        temp_filename = generate_unique_filename(save_path, base_filename, "mp4")
        filepath = os.path.join(save_path, temp_filename)
        
        response = requests.get(video_url, stream=True)
        response.raise_for_status()  # Adiciona tratamento de exceções para problemas de rede
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
            base_audio_filename = f"{post.owner_username}"
            new_filename = generate_unique_filename(save_path, base_audio_filename, "mp3")
            audio_path = os.path.join(save_path, new_filename)
            video = mp.VideoFileClip(filepath)
            video.audio.write_audiofile(audio_path)
            video.close()
            os.remove(filepath)
        else:
            # Manter como vídeo
            new_filename = generate_unique_filename(save_path, base_filename, "mp4")
            new_path = os.path.join(save_path, new_filename)
            os.rename(filepath, new_path)
        
        
        return f"{'Áudio' if format == 'audio' else 'Vídeo'} baixado com sucesso: {new_filename}"
    except ValueError as ve:
        return f"Erro: {str(ve)}"
    except InvalidArgumentException:
        return "Erro: Post não encontrado ou privado."
    except requests.RequestException as re:
        return f"Erro de rede: {str(re)}"
    except Exception as e:
        print(f"Erro ao baixar o {'áudio' if format == 'audio' else 'vídeo'}: {str(e)}", file=sys.stderr)
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

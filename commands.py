import discord
from discord.ext import commands
import yt_dlp
import os
import shlex
import subprocess
from utils import process_cover_image, zip_file, get_random_horse_gif

@commands.command()
async def hello(ctx):
    await ctx.send(f'Sup dawg {ctx.author.name}!')

@commands.command()
async def mp3(ctx, url: str, *, flags: str = ""):
    args = shlex.split(flags)
    title = artist = album = None
    cover_path = original_cover_path = final_mp3_path = None

    for i, arg in enumerate(args):
        if arg == '--title' and i + 1 < len(args):
            title = args[i + 1]
        elif arg == '--artist' and i + 1 < len(args):
            artist = args[i + 1]
        elif arg == '--album' and i + 1 < len(args):
            album = args[i + 1]

    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        if any(attachment.filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            os.makedirs('covers', exist_ok=True)
            original_cover_path = f'covers/original_{attachment.filename}'
            resized_cover_path = f'covers/resized_{attachment.filename.rsplit(".", 1)[0]}.jpg'
            await attachment.save(original_cover_path)
            await process_cover_image(original_cover_path, resized_cover_path)
            cover_path = resized_cover_path

    horse_content = await get_random_horse_gif()
    if horse_content.startswith('http'):
        embed = discord.Embed(
            title="🎵 GEDULD... download is bezig.",
            description="Hier is een paard om u bezig te houden:",
            color=0x00ff00
        )
        embed.set_image(url=horse_content)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"🎵 GEDULD... download is bezig. {horse_content}")

    ydl_opts_info = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        duration = info.get('duration', 0)

    preferredquality = '192' if duration <= 5 * 60 else '96'

    os.makedirs('downloads', exist_ok=True)
    if title and artist:
        custom_filename = f"{title} - {artist}"
        custom_filename = "".join(c for c in custom_filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
        outtmpl = f'downloads/{custom_filename}.%(ext)s'
        final_mp3_path = f'downloads/{custom_filename}.mp3'
    else:
        outtmpl = 'downloads/%(title)s.%(ext)s'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': preferredquality,
            },
            {
                'key': 'FFmpegMetadata',
            }
        ],
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not final_mp3_path:
                base = os.path.splitext(ydl.prepare_filename(info))[0]
                final_mp3_path = base + '.mp3'

        # Re-embed album art and metadata
        if cover_path:
            tagged_path = final_mp3_path.replace('.mp3', '_tagged.mp3')
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-i', final_mp3_path,
                '-i', cover_path,
                '-map', '0:a',
                '-map', '1:v',
                '-c:a', 'libmp3lame',
                '-b:a', preferredquality + 'k',
                '-c:v', 'mjpeg',
                '-id3v2_version', '3',
                '-metadata:s:v', 'title=Album cover',
                '-metadata:s:v', 'comment=Cover (front)',
            ]
            if title:
                ffmpeg_cmd += ['-metadata', f'title={title}']
            if artist:
                ffmpeg_cmd += ['-metadata', f'artist={artist}']
            if album:
                ffmpeg_cmd += ['-metadata', f'album={album}']
            ffmpeg_cmd.append(tagged_path)

            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            os.remove(final_mp3_path)
            os.rename(tagged_path, final_mp3_path)

        size = os.path.getsize(final_mp3_path)
        limit = 8 * 1024 * 1024

        if size > limit:
            await ctx.send(f"Bestand ({size / (1024*1024):.2f}MB) is te groot. We zippen het voor u.")
            zip_path = final_mp3_path + '.zip'
            zip_file(final_mp3_path, zip_path)
            await ctx.send(file=discord.File(zip_path))
            os.remove(zip_path)
        else:
            await ctx.send(file=discord.File(final_mp3_path))

    except Exception as e:
        await ctx.send(f"Gvd, tis naar de klote: stuur aub een lief bericht naar Jaan.\nError: {str(e)}")

    finally:
        for f in [cover_path, original_cover_path, final_mp3_path]:
            if f and os.path.exists(f):
                os.remove(f)
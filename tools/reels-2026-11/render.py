"""Render an HTML animation (window.render(t) -> Promise) to mp4 by piping JPEG frames to ffmpeg.
usage: python3 render.py page.html duration out.mp4 [fps] [--stills t1,t2,...]
"""
import sys, subprocess, os, asyncio
from playwright.async_api import async_playwright

html, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
fps = 30
stills = None
args = sys.argv[4:]
if args and not args[0].startswith('--'):
    fps = int(args.pop(0))
if args and args[0] == '--stills':
    stills = [float(x) for x in args[1].split(',')]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + os.path.abspath(html))
        await pg.evaluate('document.fonts.ready')
        await pg.wait_for_function('window.ready === true', timeout=120000)
        if stills:
            base = os.path.splitext(out)[0]
            for t in stills:
                await pg.evaluate(f'window.render({t})')
                await pg.screenshot(path=f'{base}_{t:05.2f}.jpg', type='jpeg', quality=85)
            await b.close(); return
        tmp = out[:-4] + '.part.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(fps), tmp], stdin=subprocess.PIPE)
        n = int(round(dur * fps))
        for i in range(n):
            await pg.evaluate(f'window.render({i / fps})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
            if i % 150 == 0: print(f'{out}: {i}/{n}', flush=True)
        ff.stdin.close(); rc = ff.wait()
        await b.close()
        if rc == 0: os.replace(tmp, out)
        else: sys.exit(rc)

asyncio.run(main())

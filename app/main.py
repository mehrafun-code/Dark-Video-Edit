"""Dark Video Edit - desktop app (pywebview window + Python/FFmpeg engine)."""
import json, os, threading, time
import webview
import engine as E

OUT = os.path.join(os.path.expanduser("~"), "Videos", "DarkVideoEdit")

class Api:
    def __init__(self): self._win = None; self.browser = None

    def _emit(self, ev, data):
        self._win.evaluate_js(f"window.onEvent({json.dumps(ev)},{json.dumps(data)})")
    def _bg(self, fn, *a):
        def w():
            try: fn(*a)
            except Exception as e: self._emit("error", {"msg": str(e)[-300:]})
        threading.Thread(target=w, daemon=True).start()

    def pick_files(self):
        kind = webview.FileDialog.OPEN if hasattr(webview, "FileDialog") else webview.OPEN_DIALOG
        r = self._win.create_file_dialog(kind, allow_multiple=True, file_types=("Video files (*.mp4;*.mov;*.mkv;*.webm)",))
        return [{"path": p, "name": os.path.basename(p), "dur": E.duration(p)} for p in (r or [])]

    def scan(self, paths): self._bg(self._scan, paths)
    def _scan(self, paths):
        shots = []
        for i, p in enumerate(paths):
            self._emit("progress", {"p": int(100 * i / len(paths)), "t": f"Scanning {os.path.basename(p)}…"})
            shots += E.make_shots(p, E.detect_kills(p), E.duration(p))
        self._emit("scan_done", {"shots": shots, "kills": sum(s["k"] for s in shots)})

    def export(self, shots, opt): self._bg(self._export, shots, opt)
    def _export(self, shots, opt):
        out = os.path.join(OUT, time.strftime("reel_%Y%m%d_%H%M%S.mp4"))
        E.build_reel(shots, out, opt, lambda p, t: self._emit("progress", {"p": p, "t": t}))
        self._emit("export_done", {"path": out})

    def info(self, url):
        try: return E.yt_info(url, self.browser)
        except Exception as e: return {"error": str(e)[-200:]}

    def download(self, req): self._bg(self._download, req)
    def _download(self, req):
        p = E.yt_download(req["url"], req["start"], req["end"], os.path.join(OUT, "downloads"), self.browser, req.get("crop"),
                          lambda p, t: self._emit("dl_progress", {"p": p, "t": t}))
        d = E.duration(p); self._emit("dl_done", {"path": p, "dur": d, "thumb": E.thumb(p, min(1, d / 2))})

    def set_browser(self, b): self.browser = b or None; return True
    def title(self, n): return E.make_title(n)
    def open_folder(self, p=None):
        os.makedirs(OUT, exist_ok=True); os.startfile(p or OUT) if hasattr(os, "startfile") else None

if __name__ == "__main__":
    api = Api()
    api._win = webview.create_window("Dark Video Edit", E.res("ui", "index.html"), js_api=api,
                                    width=1440, height=900, min_size=(1100, 700), background_color="#09080b")
    webview.start(http_server=True, private_mode=False, storage_path=os.path.join(os.path.expanduser("~"), ".darkvideoedit"))

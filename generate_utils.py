from music21 import stream, note, meter, key as m21key
import random
import dropbox
import os
import uuid

# ⬇️ 使用你的 Dropbox Token
DROPBOX_ACCESS_TOKEN = "sl.u.AFrlfZQsASSHc1VO0wauw2bY5lqwrPx4-Xs1fJZ7sNDL_JyL85NLwQnPXk3vbo9-hi83YvLvUF94B8nAkSUVWnhmZrPrC7QgYWUPQd8lcy1UPuJR9xTXvIR0OJqAXAH7Wfh4DNzqxDYGzcY1rHAZ0r8PehQldx7wSgKBUBtJ07wnt-SiXsN1cQvP9vtN7bB0o276r2zp_Bya_FT-UlIhus84epeUetBitSok3DnG7QZh5G9bw7iNRuYi7ovF8HPdfkaT1HPRR0BgTh9EaKUzVq95zSOX0bGNevMP0OONVr6a0Jaq6tCmeCh6_bRoE3xuxSsWZAYm03pNpoSWct_z04e94XxPPARQ8Yn_uM6BO_5Cwl3w4BzVgUQyHjxvB47xICeboMTcjuTOeCVloRQ0s5TMeC2Cd0DjVoaNHzOETvgZ9kul6B64q-EOhNUjju-cWQBdVnMpmWD2wpCCGLY3pZXEiahOs49YF9rGgKdTPg77QFs9LlTtuy_v6dQOjALgCAYaizaGVeNvmfuw_-cNNzH0NzRNzafIztbkfn0UqnqJWCuiPsloPvOOA42Hyr857SbWwnIRfY9WtQYJmq5gZSMsIGMra_89SJxpQiWksFQG2QINFpb6LVLinACa_CQy9JVLrzooAYsJbljOBEnim-LrpsJ2CzqwBBL_QlNKvdl7MkypyK67WdhloPG5K9pa8rZbmj7qZw0TkD3dgkXRemHde9rAf8Rh2SGoB6GcrgHL1H-vF6LI791pVPF8q10HCFOXW1kDaPtMTib3EVkHKZ-vEMjRfPdD-wuDolvcLmR_pinU3o9VmMvp2zFhXFKM_wpF13FlpeIShOEPh2Irft-anSKsZnRbGs6s2KbJEuD2P0PEUTgLxldsvL6FX2iaNe7Oq7AR7XfhNmCo_PtVmmq5S8NsJyHHnyXDA8yAN5nIA0jnyAivuDxAaHMF533jHklKfutcCeVYbFzt5_fEIwv03ASCAp0UbYMMDoCfTfZ1HH98hZnfwDwexMpXpcJP0qnFA_nxzqLxQOUSdCpyWuKliAq7-BDiIbOtKCy8WrZ_e9RZdI3yEGIFJCJEcXKU-HpxAZI66OLVBgnvt-RUFZ3puYSMMs4cVr7_Ie1hoSC35wOqdWYsq1ciFEnrBsYG4fDusv51EFAMNH29SlfrXRnWVTMluLFAM5S1MWFMk_4LeGbBNZpmApaEcZQsJOuETM94Ef5mo-5rxRZdLvB1tz7eQGOSX8_UPZdlCySGyF5CrU9mGT964V--SmtN7Y4x7HgAMgTbqVfIFun5lag3rfuRCm0tf0Md4_frs8mu4qp2MVjnt2psMjl3h7qXSLJcEgirdzdBbAsKGDGnF1nSqEziOCD2b0yYH0un_OqPK-jOvXnF56tKeBcQOs1TK8FQwE2Tl7Od0nirrtQk0_eJ6x6T"

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def generate_melody(style, key_str, time_signature, measures=8):
    score = stream.Score()

    try:
        k = m21key.Key(key_str)
    except:
        k = m21key.Key("C")

    try:
        ts = meter.TimeSignature(time_signature)
    except:
        ts = meter.TimeSignature("4/4")

    melody = stream.Part()
    melody.append(k)
    melody.append(ts)

    scale_pitches = k.getPitches()
    for _ in range(measures):
        m = stream.Measure()
        for _ in range(4):
            pitch = random.choice(scale_pitches)
            n = note.Note(pitch)
            n.quarterLength = 1.0
            m.append(n)
        melody.append(m)

    score.append(melody)

    # 儲存 musicxml 檔案
    filename = f"melody_{uuid.uuid4().hex}.musicxml"
    score.write('musicxml', fp=filename)

    # 上傳到 Dropbox
    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), f"/{filename}", mode=dropbox.files.WriteMode.overwrite)

    # 建立分享連結
    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/{filename}")
    public_url = shared_link_metadata.url.replace("?dl=0", "?dl=1")

    # 清除本地檔案（節省空間）
    os.remove(filename)

    return public_url

from music21 import stream, note, meter, key as m21key
import random
import dropbox
import os
import uuid

# ⬇️ 使用你的 Dropbox Token
DROPBOX_ACCESS_TOKEN = "sl.u.AFqo5SvLeHb4avr8UMpz3BgocChXph91pn4HvIYsjyWyOLNPdlcy7qgs-Bgp0nQH-WutpkcjW9Te989411HxU2eZH8e_lXbbQlerWlah1fpVfkbzXy7SmmVp44-584LK1Zr6UJnZO6dK3yDl_WdVJqYEpvdynAccrrsJFeAlC-oYMth52a4_Rto9m4Jbpg18UyTxCCLUM7k0okPztnCt8kKiYQ7TULuxo19C9XFwFlFrcgJlceb2SRyiSQcI0k8hv7BW90tIFUtfvCYrhI2pqCH1ku_Xx_J7D1-a0yYv1AePNrp7ObDNPLBag3NFksaX2X6mH743E63vvDkaIpVCke7BFvEDc6VDGzAvmc5XtRncUx-AVNtM6EJwIOBTY0-MeAmwomz1AVUiXJSCWbSApCqkvaD2vad0KP6mbflitUcwjZB4g_feXExEd88VGkzfWJEnMfRu_UJY93hEShqqgFfVXHe5QlWj75f0E6fWPxRYS-OQIkcXJsON51xu-Rjuq-q33B6AA_OpygDPP5rJzsPZWn5wE_zqgwWn5I7Gn5m9qS0hKE2fPUwBhrQDs3Qpr3zhxLV4peHtjAveiKsFtphlSfJLAYOeCb8pBMRB6XL0DcEC2ISpT0PkjaxHQoHjsFHYt2senE6eJlzD0SeiT_Gm5yUDs9CysMIaNx7EyVSr8p4dLPbQbjswaMhVkp7fd_PnyLRr-JfWgfjq2jP06_P8Gxtzy-V6ClF32Vmz0Kkgl5IXYZYfv42e6AFfpJ7ANPwRrMBAZyeKbR54Ldg6rQUlO_SMElmHIFIoH8WgSLXN5wunkbL_eu6bLCPCICl9NYB4xwY4v3kTSJfnMh1RPlrTGTTQ_bVy1TRqLgK3uUmE9aIf1MOp1K6NPkPAZ5O8RTJ2-KL7hD7MqsZmaUtpWjBoVwTN2ZiEfkgrXMs7YkRXT6ijVU_NcJ4_4gv1vhCWvlMeM0RY4V3VWuFoZ4W9Fvq0Iud4ZCQ0MsXA4of8Hzf6mpdu134b7xnY1-GUnxGvuK2caKEE4krk5P390-MCavXy6LZXFJJomye8ldIy2YfTh5-e4yPcNwgiw3HgoOM6TBA-twPaHbImY6As3zF73QQJowtVmw9HzB5AVGUKzNm2Mbh4koVrmBrdqJyBtdSgo8pOrZ1BrC2ggV0oJLpcwWRcgzjCk7b1l7tOxTwNtslJvpJdz1qdjJSa1SwH8M-x0JCXg3WgBZRRZ-WM1rjIkjfG3gWQa_m5p99h7k1EvpFNz6Cid-obwxNugdcDLwSl26Q07gON7l3fJWDAKf5T1FN6TaVlkKKNTVT3Ba-JsQnwr9ykWhuMiNSHd5qSQDx78Ow-cKYcb_nVsKjeXvWhIKg5EPpI3MDuOjiChZUXJmq02FREcY-s8CKuMSlWgg1rXbcDXlaq5c_wH643dm7x6OTD"

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

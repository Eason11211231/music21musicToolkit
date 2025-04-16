from music21 import converter, analysis, key
import re

def analyze_musicxml(musicxml_string):
    try:
        score = converter.parse(musicxml_string)

        # 主要調性分析
        k = score.analyze("key")
        result = {
            "detectedKey": str(k),
            "isMinor": k.mode == "minor",
            "modulations": [],
            "cadences": [],
            "tritoneSubstitutions": []
        }

        # 偵測轉調（找每個小節的調性）
        measure_keys = []
        for m in score.parts[0].getElementsByClass('Measure'):
            this_key = m.analyze("key")
            measure_keys.append(str(this_key))

        # 對比是否發生轉調
        unique_keys = list(set(measure_keys))
        if len(unique_keys) > 1:
            result["modulations"] = unique_keys

        # 簡單終止式偵測（以 V-I 進行為主）
        chords = score.chordify()
        roman = analysis.romanNumeral.romanNumeralFromChord
        prev_rn = None
        for c in chords.recurse().getElementsByClass('Chord'):
            try:
                rn = roman(c, k)
                if prev_rn == "V" and rn.figure == "I":
                    result["cadences"].append("Authentic cadence found")
                prev_rn = rn.figure
            except:
                continue

        # Tritone substitution 偵測（簡單版）
        tritone_regex = re.compile(r'(bII7|bVI7|bIII7)')
        for chord_string in measure_keys:
            if tritone_regex.search(chord_string):
                result["tritoneSubstitutions"].append(chord_string)

        return result

    except Exception as e:
        return {"error": str(e)}

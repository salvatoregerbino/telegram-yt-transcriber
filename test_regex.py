import re

youtube_regex_pattern = r'^(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|live\/|v\/|shorts\/)([a-zA-Z0-9_-]{11})|youtu\.be\/([a-zA-Z0-9_-]{11}))(?:\S*)?$'

# Costruiamo la stringa 'https://www.youtube.com/watch?v=dQw4w9WgXcqqqqq12:58' (42 caratteri) programmaticamente
# usando i suoi codici ordinali Unicode (ASCII in questo caso).
# 'h', 't', 't', 'p', ':', '/', '/', 'g', 'o', 'o', 'g', 'l', 'e', 'u', 's', 'e', 'r', 'c', 'o', 'n', 't', 'e', 'n', 't', '.', 'c', 'o', 'm', '/', 'y', 'o', 'u', 't', 'u', 'b', 'e', '.', 'c', 'o', 'm', '/', '5'
char_codes_for_intended_url = [
    104, 116, 116, 112, 58, 47, 47, 103, 111, 111, 103, 108, 101, 117, 115, 101, 114, 99, 111, 110, 116, 101, 110, 116, 46, 99,
    111, 109, 47, 121, 111, 117, 116, 117, 98, 101, 46, 99, 111, 109, 47, 53
]
test_url_original = "".join([chr(code) for code in char_codes_for_intended_url])
expected_length = 42 # Lunghezza attesa per 'https://www.youtube.com/watch?v=dQw4w9WgXcqqqqq12:58'

print("--- INIZIO TEST CON STRINGA COSTRUITA PROGRAMMATICAMENTE ---")
print(f"URL di test (repr): {repr(test_url_original)}")
print(f"Lunghezza URL (len): {len(test_url_original)}")

print("\nAnalisi Caratteri (Codice Ordinale Unicode):")
char_details = []
for i, char_in_string in enumerate(test_url_original):
    char_details.append(f"Indice {i}: '{repr(char_in_string)}' - Codice Dec: {ord(char_in_string)} - Codice Hex: {hex(ord(char_in_string))}")

for i in range(0, len(char_details), 5):
    print(" | ".join(char_details[i:i+5]))

if len(test_url_original) != expected_length:
    print(f"\nATTENZIONE: La lunghezza attesa per la stringa costruita programmaticamente era {expected_length}, ma len() riporta {len(test_url_original)}.")
    print("Questo indicherebbe un problema molto profondo.")
else:
    print(f"\nLunghezza della stringa ({len(test_url_original)}) è quella attesa ({expected_length}).")


print("\n--- RISULTATO DEL MATCH REGEX ---")
match_object = re.search(youtube_regex_pattern, test_url_original)

if match_object:
    print("RISULTATO: MATCH TROVATO!")
    video_id = None
    if match_object.group(1):
        video_id = match_object.group(1)
        print(f"ID (da gruppo 1): {video_id}")
    elif match_object.group(2):
        video_id = match_object.group(2)
        print(f"ID (da gruppo 2): {video_id}")
    
    print(f"Oggetto Match completo (repr): {repr(match_object)}")
    print(f"Stringa matchata (group(0)) (repr): {repr(match_object.group(0))}")
    print(f"Lunghezza stringa matchata: {len(match_object.group(0))}")
    print(f"Span del match: {match_object.span()}")
    print(f"Tutti i gruppi catturati: {match_object.groups()}")
else:
    print("RISULTATO: NESSUN MATCH TROVATO.")

print("--- FINE TEST ---")

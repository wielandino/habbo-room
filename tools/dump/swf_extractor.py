import subprocess
import os

def extract_all_from_swf(swf_file, output_folder):
    """Extrahiert PNGs UND Binarys"""
    
    if not os.path.exists(swf_file):
        print(f"FEHLER: Datei nicht gefunden: {swf_file}")
        return
    
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. Info anzeigen
    command = f"swfextract -i {swf_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    # 2. Extrahiere PNGs
    png_ids = [1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 22, 23]
    
    print(f"\n=== Extrahiere {len(png_ids)} PNGs ===")
    for i, png_id in enumerate(png_ids):
        output_file = os.path.join(output_folder, f"sprite_{i:03d}_id{png_id}.png")
        command = f"swfextract -p {png_id} {swf_file} -o {output_file}"
        subprocess.run(command, shell=True, capture_output=True)
        if os.path.exists(output_file):
            print(f"✓ sprite_{i:03d}_id{png_id}.png")
    
    # 3. Extrahiere Binarys (XML-Dateien)
    binary_ids = [2, 4, 6, 17, 21]
    
    print(f"\n=== Extrahiere {len(binary_ids)} Binarys (XML) ===")
    for binary_id in binary_ids:
        output_file = os.path.join(output_folder, f"binary_id{binary_id}.bin")
        command = f"swfextract -b {binary_id} {swf_file} -o {output_file}"
        subprocess.run(command, shell=True, capture_output=True)
        
        if os.path.exists(output_file):
            # Versuche als XML zu lesen
            try:
                with open(output_file, 'rb') as f:
                    content = f.read()
                    
                # Wenn es XML ist, speichere als .xml
                if b'<?xml' in content or b'<manifest' in content or b'<assets' in content:
                    xml_file = output_file.replace('.bin', '.xml')
                    with open(xml_file, 'wb') as f:
                        f.write(content)
                    print(f"✓ binary_id{binary_id}.xml (XML-Datei)")
                    os.remove(output_file)  # Lösche die .bin Version
                else:
                    print(f"✓ binary_id{binary_id}.bin (Binärdatei)")
            except:
                print(f"✓ binary_id{binary_id}.bin")
    
    print(f"\nFertig! Alle Dateien in: {output_folder}")

# Verwende den relativen Pfad zum Script
script_dir = os.path.dirname(os.path.abspath(__file__))
swf_path = os.path.join(script_dir, "nft_a0club_sofa.swf")
output_path = os.path.join(script_dir, "sofa_sprites")

extract_all_from_swf(swf_path, output_path)
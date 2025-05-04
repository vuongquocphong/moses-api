import xmlrpc.client

def batch_translate(sentences, server_url="http://localhost:8080/RPC2"):
    server = xmlrpc.client.ServerProxy(server_url)
    results = []

    for sentence in sentences:
        params = {'text': sentence}
        try:
            response = server.translate(params)
            results.append(response.get('text', ''))  # fallback to empty string if 'text' missing
        except Exception as e:
            results.append(f"[Error: {e}]")  # include error for debugging
    return results

def preprocess_snt_for_transliteration(replace_dict, text: str):
    # Preprocess the text if necessary (e.g., remove unwanted characters)
    for char in text:
        # Check if the character is in Basic Multilingual Plane (BMP)
        if ord(char) <= 65535:
            continue
        # If not, check if it is in the replace dictionary
        if char in replace_dict.keys():
            text = text.replace(char, replace_dict[char])
            print(replace_dict[char])
        else:
            # If the character is not in the replace dictionary, replace it with a space
            text = text.replace(char, ' ')
    return text    

# Example usage:
if __name__ == "__main__":
    sample_dict = {
        '𦏁': 'hi',
    }
        
    lines = [
        "大 越 史 記 外 紀 全 書 卷 之 一",
        "朝 列 大 夫 國 子 監 司 業 兼 史 官 修 撰 臣 吳 士 連 編",
        "按 黄 帝 時 建 萬 國 以 交 趾 界 於 西 南 遠 在 百 粤 之 表",
        "堯 命 𦏁 氏 宅 南 交 定 南 方 交 趾 之 地",
    ]
    
    preprocessed_lines = [preprocess_snt_for_transliteration(sample_dict, line) for line in lines]
    print("Preprocessed Lines:")
    for line in preprocessed_lines:
        print(line)

    translations = batch_translate(preprocessed_lines)
    for original, translated in zip(lines, translations):
        print(f"{original}\n→ {translated}\n")

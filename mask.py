import pandas as pd
import re

def mask_except_keywords(s, keywords, mask_char='*'):
    # 正規表現 overlay|interstitial が完成
    pattern = '|'.join(map(re.escape, keywords))
    # partsは['aaa_','_bbb']となる(aaa_overlay_bbb だった場合)
    parts = re.split(pattern, s)
    # mask_char（マスクに使用する文字、*）を len(part)（partの文字列の長さ）回だけ繰り返す → ['****','****']となる
    masked_parts = [mask_char*len(part) if part else '' for part in parts]
    # overlay|interstitial にmatchするものをリストに格納する
    matches = re.findall(pattern, s)
    # masked_partsとmatchesの結合/　+ masked_parts[-1]は配列最後の要素を追加している
    result = ''.join(sum(zip(masked_parts, matches), ())) + masked_parts[-1]
    return result

# データを読み込む
df = pd.read_csv('GAMSampleData_1.csv')

# マスキングしたいカラムを選択
column = 'ad_unit'

# マスキングのロジックを適用（ここでは "overlay" または "interstitial" を含む文字列以外を '*' でマスキング）
keywords = ["overlay", "interstitial"]
df[column] = df[column].apply(lambda x: mask_except_keywords(str(x), keywords))

# ファイルに書き出す
df.to_csv('GAMSampleData_1_masked.csv', index=False)
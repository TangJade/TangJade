import pandas as pd
import re
from pathlib import Path
from html import unescape

BASE_DIR=Path(__file__).resolve().parent.parent

input_path=BASE_DIR/"data"/"raw"/"amazon_reviews.csv"
output_path=BASE_DIR/"data"/"processed"/"cleaned_with_count.csv"

output_path.parent.mkdir(parents=True,exist_ok=True)

df=pd.read_csv(input_path)

def clean_text(text):
    text=unescape(str(text))
    text=re.sub(r"<[^>]+>"," ",text)
    text=re.sub(r"\s+"," ",text)
    return text.strip()

df=df.dropna(subset=["text"]).copy()
df["text"]=df["text"].apply(clean_text)
df=df[df["text"]!=""].copy()

result=(
    df.groupby(["labels","text"],dropna=False)
    .size()
    .reset_index(name="count")
)

result=result.sort_values(
    by=["count","labels"],
    ascending=[False,True]
).reset_index(drop=True)

result.insert(0,"id",range(1,len(result)+1))

result.to_csv(output_path,index=False,encoding="utf-8-sig")

print("原始记录数：",90000)
print("清洗后记录数：",len(df))
print("合并后唯一的记录数：",len(result))
print("统计的总出现数：",result["count"].sum())
print("输出文件：",output_path)

print("\n出现次数最多的前10条评论：")
print(
    result.sort_values("count",ascending=False)
    .head(10)
    .to_string(index=False)
)

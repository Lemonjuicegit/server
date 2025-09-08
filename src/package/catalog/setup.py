import pandas as pd
import os

def get_folder_size(folder_path):
    """计算目录下文件或目录的大小

    Args:
        folder_path (Path): 要计算的目录路径

    Returns:
        float
    """
    df = pd.DataFrame(columns=["folder_path", "size_bytes", "size_kb", "size_mb", "size_gb"])
    names = list(folder_path.iterdir())
    for item in names:
        total_size = 0
        for dirpath, _, filesin in os.walk(item):
            for file in filesin:
                file_path = os.path.join(dirpath, file)
                total_size += os.path.getsize(file_path)

        df.loc[len(df)] = [
            item.name,
            total_size,
            total_size / 1024,
            total_size / (1024 * 1024),
            total_size / (1024 * 1024 * 1024),
        ]
    
    return df

if __name__ == '__main__':
    from pathlib import Path

    res = get_folder_size(Path(r"C:\Users\Administrator\AppData"))
    res.to_csv(r"E:\工作文档\测试导出数据\大小.csv")

    



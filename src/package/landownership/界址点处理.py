import geopandas as gpd


class ZDTidyUp():
    def __init__(self,gdb) -> None:
        """
        初始化方法，用于从地理数据库中加载宗地、界址点和所有宗地数据。
        
        参数:
            gdb (str): 地理数据库的路径。
        """
        self.ZD = gpd.read_file(gdb,layer="宗地")
        self.JZD = gpd.read_file(gdb,layer="JZD")
        self.ZD_ALL = gpd.read_file(gdb,layer="ZD_ALL")
        
    def intersection(self,jzd_gdf_):
        """
        该方法用于检查界址点之间的交点关系，并整理宗地数据。
        
        参数:
            jzd_gdf_ (GeoDataFrame): 包含界址点的地理数据框。
        """
        for index,row in jzd_gdf_.iterrows():
            QLRMC = self.ZD[self.ZD.ZDDM.isin(jzd_gdf_.ZDDM)].QLRMC.values[0]
            ZDDM = jzd_gdf_.ZDDM.values[0]
            if index == 0:
                b_jzd,h_xljzd,q_xljzd = self.adjacent_jzdzddm(row)
                self.JZX.loc[self.JZX.shape[0],'ZDDM'] = ZDDM
                self.JZX.loc[self.JZX.shape[0]-1,'QLRMC'] = QLRMC
                if XLQLRZDDM := list(set(b_jzd.ZDDM) & set(q_xljzd.ZDDM)):
                    self.JZX.loc[self.JZX.shape[0]-1,'LZQLRMC'] = self.JZD_All[self.JZD_All.ZDDM == XLQLRZDDM[0]].QLRMC.values[0]
                self.JZX.loc[self.JZX.shape[0]-1,'QSDH'] = jzd_gdf .JZD_NEW.values[0]
                self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'] = []
                self.JZX.loc[self.JZX.shape[0]-1,'INDEX'] = jzd_gdf_.at[index,'INDEX']
                continue
            if index == jzd_gdf_.shape[0]-1:
                # 终点界址点
                b_jzd,h_xljzd,q_xljzd = self.adjacent_jzdzddm(row)
                if list(set(h_xljzd.ZDDM) & set(q_xljzd.ZDDM)) or (b_jzd.shape[0] == 0):

                    self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'].append(row.JZD_NEW)
                else:
                    self.JZX.loc[self.JZX.shape[0],'ZDDM'] = ZDDM
                    self.JZX.loc[self.JZX.shape[0]-1,'QLRMC'] = QLRMC
                    if XLQLRZDDM := list(set(b_jzd.ZDDM) & set(q_xljzd.ZDDM)):
                        self.JZX.loc[self.JZX.shape[0]-1,'LZQLRMC'] = self.JZD_All[self.JZD_All.ZDDM == XLQLRZDDM[0]].QLRMC.values[0]
                    self.JZX.loc[self.JZX.shape[0]-1,'QSDH'] = row.JZD_NEW
                    self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'] = []
                    self.JZX.loc[self.JZX.shape[0]-2,'ZZDH'] = row.JZD_NEW
                    self.JZX.loc[self.JZX.shape[0]-1,'INDEX'] = jzd_gdf_.at[index,'INDEX']
                
                self.JZX.loc[self.JZX.shape[0]-1,'ZZDH'] = jzd_gdf_.at[0,'JZD_NEW']
                continue
            b_jzd,h_xljzd,q_xljzd = self.adjacent_jzdzddm(row)
            if list(set(h_xljzd.ZDDM) & set(q_xljzd.ZDDM))  or (b_jzd.shape[0] == 0):
                self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'].append(row.JZD_NEW)
            else:
                self.JZX.loc[self.JZX.shape[0],'ZDDM'] = ZDDM
                self.JZX.loc[self.JZX.shape[0]-1,'QLRMC'] = QLRMC
                if XLQLRZDDM := list(set(b_jzd.ZDDM) & set(q_xljzd.ZDDM)):
                    self.JZX.loc[self.JZX.shape[0]-1,'LZQLRMC'] = self.JZD_All[self.JZD_All.ZDDM == XLQLRZDDM[0]].QLRMC.values[0]
                self.JZX.loc[self.JZX.shape[0]-1,'QSDH'] = row.JZD_NEW
                self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'] = []
                self.JZX.loc[self.JZX.shape[0]-2,'ZZDH'] = row.JZD_NEW
                self.JZX.loc[self.JZX.shape[0]-1,'INDEX'] = jzd_gdf_.at[index,'INDEX']
                
    def zdfield(self,tfhgdb,save):
        """
        该方法用于向宗地数据中添加额外字段并保存结果。
        
        参数:
            tfhgdb (str): 包含TFH数据的地理数据库路径。
            save (str): 处理后的宗地数据保存路径。
        """
        tfhshp = gpd.read_file(tfhgdb,layer='宗地_tfh')
        self.ZD['']
        def tfhs(row):
            return '、'.join(set(tfhshp[tfhshp.ZDDM == row.ZDDM].NEWMAPNO.values))
        self.ZD.TFH = self.ZD.apply(tfhs,axis=1)
        
        self.ZD.to_excel(save)
    
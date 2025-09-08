import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import MultiPolygon,mapping,LineString
from . import groupby
class Ownership:
    """
    该类用于处理和分析所有权数据，包括宗地（ZD）和界址点（JZD）数据。
    
    属性:
    - ZD: 宗地数据，填充为空字符串以处理缺失值。
    - JZD: 界址点数据，计算并添加X和Y坐标列。
    - JZD_All: 所有界址点数据，未进行过滤。
    - zdcount: 宗地数量。
    - qlrcount: 权利人数量。
    - JZX: 用于存储界址线数据的DataFrame。
    - JZD: 经过处理的界址点数据，按宗地代码和排序字段排序。
    - jzd_boundary: 界址点边界数据，用于后续处理。
    """
    def __init__(self,gdbpath):
        """
        初始化Ownership类，读取并处理宗地和界址点数据。
        
        参数:
        - gdbpath: 数据库路径。
        """
        self.ZD = gpd.read_file(gdbpath,layer='ZD').fillna('')
        # self.ZD = self.ZD[self.ZD.QLRMC == '']
        self.JZD = gpd.read_file(gdbpath,layer='JZD').fillna('')
        self.JZD['X'] = np.round(self.JZD.geometry.x*100).astype('int64')
        self.JZD['Y'] = np.round(self.JZD.geometry.y*100).astype('int64')
        # self.JZD = self.JZD[self.JZD.QLRMC == '']
        # self.get_coordinates(self.ZD)
        self.JZD_All = gpd.read_file(gdbpath,layer='ZD_All')
        # self.JZD_All = self.JZD_All[self.JZD_All.ZDDM == 'JA3711']
        self.zdcount = self.ZD.shape[0]
        self.qlrcount = self.ZD.QLRMC.drop_duplicates().shape[0]
        self.JZX = pd.DataFrame(columns=('ZDDM','QLRMC','LZQLRMC','QSDH','ZJDH','ZZDH','INDEX','BXZ','BCM','BSM','XLXZ','XLCM','XLSM'))
        self.JZD,self.jzd_boundary = self.get_jzd_boundary()
        self.JZD.sort_values(by=['ZDDM','PX'],inplace=True)
    def adjacent_jzdzddm(self,jzd)->{pd.DataFrame,pd.DataFrame,pd.DataFrame}:
        """
        获取相邻界址点的宗地代码。
        
        参数:
        - jzd: 当前界址点。
        
        返回:
        - b_xljzd: 边界上的相邻界址点。
        - h_xljzd: 后面相邻的界址点。
        - q_xljzd: 前面相邻的界址点。
        """
        # 相邻界址点
        x = jzd.X
        y = jzd.Y
        b_xljzd = self.jzd_boundary[(self.jzd_boundary.X == x) & (self.jzd_boundary.Y == y) & ~(self.jzd_boundary.ZDDM== jzd.ZDDM)]
        b_jzd = self.jzd_boundary[(self.jzd_boundary.ZDDM == jzd.ZDDM) & (self.jzd_boundary.INDEX == jzd.INDEX)]
        JZDH = jzd.JZDH
        if not JZDH:
            h_boundary_x = b_jzd.iloc[-1].X
            h_boundary_y = b_jzd.iloc[-1].Y
            q_boundary_x = b_jzd.iloc[JZDH+1].X
            q_boundary_y = b_jzd.iloc[JZDH+1].Y
            h_xljzd = self.jzd_boundary[(self.jzd_boundary.X == h_boundary_x) & (self.jzd_boundary.Y == h_boundary_y) & ~(self.jzd_boundary.ZDDM == jzd.ZDDM)] # 后面相邻界址点
            q_xljzd = self.jzd_boundary[(self.jzd_boundary.X == q_boundary_x) & (self.jzd_boundary.Y == q_boundary_y) & ~(self.jzd_boundary.ZDDM == jzd.ZDDM)] # 前面相邻界址点
        elif JZDH == b_jzd.iloc[-1].JZDH:
            h_boundary_x = b_jzd.iloc[JZDH-1].X
            h_boundary_y = b_jzd.iloc[JZDH-1].Y
            q_boundary_x = b_jzd.iloc[0].X
            q_boundary_y = b_jzd.iloc[0].Y
            h_xljzd = self.jzd_boundary[(self.jzd_boundary.X == h_boundary_x) & (self.jzd_boundary.Y == h_boundary_y) & ~(self.jzd_boundary.ZDDM == jzd.ZDDM)] # 后面相邻界址点
            q_xljzd = self.jzd_boundary[(self.jzd_boundary.X == q_boundary_x) & (self.jzd_boundary.Y == q_boundary_y) & ~(self.jzd_boundary.ZDDM == jzd.ZDDM)] # 前面相邻界址点
        else:
            h_boundary_x = b_jzd.iloc[JZDH-1].X
            h_boundary_y = b_jzd.iloc[JZDH-1].Y
            q_boundary_x = b_jzd.iloc[JZDH+1].X
            q_boundary_y = b_jzd.iloc[JZDH+1].Y
            h_xljzd = self.jzd_boundary[(self.jzd_boundary.X == h_boundary_x) & (self.jzd_boundary.Y == h_boundary_y) & ~(self.jzd_boundary.ZDDM == jzd.ZDDM)] # 后面相邻界址点
            q_xljzd = self.jzd_boundary[(self.jzd_boundary.X == q_boundary_x) & (self.jzd_boundary.Y == q_boundary_y) & ~(self.jzd_boundary.ZDDM == jzd.ZDDM)] # 前面相邻界址点 
        return b_xljzd,h_xljzd,q_xljzd
 
    def set_zddm(self,zddm):
        """
        设置宗地代码，过滤ZD和JZD数据框。
        
        参数:
        - zddm: 宗地代码列表。
        """
        self.ZD = self.ZD[self.ZD.ZDDM.isin(zddm)]
        self.JZD = self.JZD[self.JZD.ZDDM.isin(zddm)]
        
    def get_coordinates(self,one_gdf):
        """
        获取坐标数据并整理成DataFrame格式。
        
        参数:
        - one_gdf: 一行GeoDataFrame数据或GeoSeries。
        
        返回:
        - coor_df: 包含坐标的DataFrame。
        """

        if not (isinstance(one_gdf, pd.DataFrame) or isinstance(one_gdf, pd.Series)):
            raise TypeError(f'传入的是:{type(one_gdf.geometry.values[0])},需要的是{type(MultiPolygon())}|{type(gpd.GeoDataFrame())}|{type(pd.Series())}')
        if isinstance(one_gdf, pd.Series):
            if isinstance(one_gdf.geometry, MultiPolygon):
                data = mapping(one_gdf.geometry)
                zddm = one_gdf.ZDDM
            else:
                raise TypeError(f'传入的是:{type(one_gdf.geometry)},需要的是{type(MultiPolygon())}')
        if isinstance(one_gdf, pd.DataFrame):
            if one_gdf.shape[0] > 1:
                raise ValueError(f'只接收一行数据,但传入了{one_gdf.shape[0]}行数据')
            if isinstance(one_gdf.geometry.values[0], MultiPolygon):
                data = mapping(one_gdf.geometry.values[0])
                zddm = one_gdf.ZDDM.values[0]
            else:
                raise TypeError(f'传入的是:{type(one_gdf.geometry.values[0])},需要的是{type(MultiPolygon())}')
        def add_index(x_y,value,V):
            # if V == 87:
            #     pass
            temp = [zddm,*(np.round(x_y*100)).astype('int64'),value,V]
            return temp
        
        # coor_df = pd.DataFrame(columns=['ZDDM','X','Y','INDEX','JZDH'])

        for index,value in enumerate(data['coordinates'][0]):
            if not index:
                coor_df = pd.DataFrame([add_index(np.array(x),index,V) for V,x in enumerate(value[:len(value)-1])],columns=['ZDDM','X','Y','INDEX','JZDH'])
            else:
                coor_df = pd.concat([coor_df,pd.DataFrame([add_index(np.array(x),index,V) for V,x in enumerate(value[:len(value)-1])],columns=['ZDDM','X','Y','INDEX','JZDH'])],ignore_index=True)
        return coor_df
    
    def get_coordinates_index(self,coordinates):
        """
        获取坐标索引。
        
        参数:
        - coordinates: 坐标数据。
        
        返回:
        - 坐标索引的Series。
        """
        return coordinates.INDEX.drop_duplicates(ignore_index=True)
    
    def get_zddm(self):
        """
        获取宗地代码。
        
        返回:
        - 宗地代码的Series。
        """
        return self.ZD.ZDDM.drop_duplicates(ignore_index=True)
    
    def get_jzd_boundary(self):
        """
        获取界址点边界信息。
        
        返回:
        - 合并后的界址点和坐标数据。
        - 坐标数据。
        """
        # 这是一个将界址点与边界信息连接的方法
        _coordinates = pd.DataFrame()
        for index,row in self.JZD_All.iterrows():
            if index == 0:
                _coordinates = self.get_coordinates(row)
            else:
                _coordinates = pd.concat([_coordinates,self.get_coordinates(row)],ignore_index=True)
        
        self.JZD[~self.JZD.X.isin(_coordinates.X) | ~self.JZD.Y.isin(_coordinates.Y)].to_excel('没匹配上的界址点.xlsx')
        return pd.merge(self.JZD,_coordinates,on=['ZDDM','X','Y'], how='inner'),_coordinates
        
    def add_jzx(self,jzd_gdf_):
        """
        添加界址线数据。
        
        参数:
        - jzd_gdf_: 界址点数据。
        """
        for index,row in jzd_gdf_.iterrows():
            QLRMC = self.ZD[self.ZD.ZDDM.isin(jzd_gdf_.ZDDM)].QLRMC.values[0]
            ZDDM = jzd_gdf_.ZDDM.values[0]
            b_jzd,h_xljzd,q_xljzd = self.adjacent_jzdzddm(row)
            if index == 0:

                self.JZX.loc[self.JZX.shape[0],'ZDDM'] = ZDDM
                self.JZX.loc[self.JZX.shape[0]-1,'QLRMC'] = QLRMC
                if XLQLRZDDM := list(set(b_jzd.ZDDM) & set(q_xljzd.ZDDM)):
                    self.JZX.loc[self.JZX.shape[0]-1,'LZQLRMC'] = self.JZD_All[self.JZD_All.ZDDM == XLQLRZDDM[0]].QLRMC.values[0]
                self.JZX.loc[self.JZX.shape[0]-1,'QSDH'] = jzd_gdf_.JZD_NEW.values[0]
                self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'] = []
                self.JZX.loc[self.JZX.shape[0]-1,'INDEX'] = jzd_gdf_.at[index,'INDEX']
                continue
            if index == jzd_gdf_.shape[0]-1:
                # 终点界址点
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
                if self.JZX.loc[self.JZX.shape[0]-1,'QSDH'] == jzd_gdf_.at[0,'JZD_NEW']:
                    self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'].remove(jzd_gdf_.tail(1).JZD_NEW.values[0])
                    self.JZX.loc[self.JZX.shape[0]-1,'ZZDH'] = jzd_gdf_.tail(1).JZD_NEW.values[0]
                    self.JZX.loc[self.JZX.shape[0],'ZDDM'] = ZDDM
                    self.JZX.loc[self.JZX.shape[0]-1,'QLRMC'] = QLRMC
                    if XLQLRZDDM := list(set(b_jzd.ZDDM) & set(q_xljzd.ZDDM)):
                        self.JZX.loc[self.JZX.shape[0]-1,'LZQLRMC'] = self.JZD_All[self.JZD_All.ZDDM == XLQLRZDDM[0]].QLRMC.values[0]
                    self.JZX.loc[self.JZX.shape[0]-1,'QSDH'] = jzd_gdf_.tail(1).JZD_NEW.values[0]
                    self.JZX.loc[self.JZX.shape[0]-1,'ZJDH'] = []
                    self.JZX.loc[self.JZX.shape[0]-1,'INDEX'] = jzd_gdf_.at[index,'INDEX']
                self.JZX.loc[self.JZX.shape[0]-1,'ZZDH'] = jzd_gdf_.at[0,'JZD_NEW']
                continue
            
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
    def to_JZXexcel(self,path):
        """
        将JZX数据导出到Excel文件中。

        参数:
        - path: str, 输出文件的路径。
        """
        self.JZX.to_excel(path,index=False)
    
    def add_jzx_all(self):
        """
        为所有界址点添加JZX信息。
        该函数会获取所有界址点代码，然后为每个界址点代码对应的界址点添加JZX信息。
        使用get_coordinates_index函数获取坐标索引，并通过add_jzx函数为每个界址点添加JZX信息。
        """
        zddm_df = self.get_zddm()
        for zddm in zddm_df:
            coordinates_index = self.get_coordinates_index(self.JZD[self.JZD.ZDDM == zddm])
            for index in coordinates_index:
                sel_jzd = self.JZD[(self.JZD.ZDDM == zddm) & (self.JZD.INDEX == index)].reset_index()
                self.add_jzx(sel_jzd)
            yield f"正在生成:{zddm}"
    
    def to_jzxshp(self,savepath):
        """
        将JZX数据导出为Shapefile格式文件。
        参数:
        - savepath: str, 输出文件的路径。

        该函数首先对JZX数据进行格式化，然后将其转换为GeoDataFrame格式，以便于导出为Shapefile格式。
        同时，该函数还会生成一个包含界址点信息的DataFrame，并根据这些信息构建LineString对象，作为界址线数据的一部分。
        """
        JZXDF = self.ZJDH_format()
        JZXDF['ZDDM_INDEX'] = JZXDF.ZDDM.str.cat(JZXDF.INDEX.astype(str))
        jzx = gpd.GeoDataFrame(columns=[*JZXDF.columns,'geometry'],crs=self.ZD.crs) # type: ignore
        zd_node = pd.DataFrame(columns=('QLRMC','ZDDM','INDEX','ZDDM_INDEX','N','X','Y'))
        for index,row in self.ZD.iterrows():
            geojson = mapping(row.geometry)
            for index,value in enumerate(geojson['coordinates'][0]):
                zd_node_row = [{'QLRMC':row.QLRMC,'ZDDM':row.ZDDM,'INDEX':index,'ZDDM_INDEX':row.ZDDM+str(index),'N':n+1,'X':coor[0],'Y':coor[1]} for n,coor in enumerate(value[:len(value)-1])]
                if not zd_node.shape[0]:
                    zd_node = pd.DataFrame(zd_node_row)
                else:
                    zd_node = pd.concat([zd_node,pd.DataFrame(zd_node_row)],ignore_index=True)
        zd_node['int_X'] = np.round(zd_node.X*100).astype('int64')
        zd_node['int_Y'] = np.round(zd_node.Y*100).astype('int64')
        for index,value in JZXDF.iterrows():
            ZD_boundary = zd_node[zd_node.ZDDM_INDEX == value.ZDDM_INDEX].reset_index()
            q_jzd = self.JZD[(self.JZD.ZDDM ==value.ZDDM) & (self.JZD.JZD_NEW == value.QSDH)]
            z_jzd = self.JZD[(self.JZD.ZDDM ==value.ZDDM) & (self.JZD.JZD_NEW == value.ZZDH)]
            q_line_index = ZD_boundary[(ZD_boundary.int_X==q_jzd.X.values[0]) & (ZD_boundary.int_Y==q_jzd.Y.values[0])].index[0]
            z_line_index = ZD_boundary[(ZD_boundary.int_X==z_jzd.X.values[0]) & (ZD_boundary.int_Y==z_jzd.Y.values[0])].index[0]
            xy_list = []
            if q_line_index>=z_line_index:
                max_index = np.max(ZD_boundary.index.values)
                q_line_df = ZD_boundary.iloc[q_line_index:max_index+1]
                h_line_df = ZD_boundary.iloc[0:z_line_index+1]
                xy_list = list(zip(list(q_line_df.X),list(q_line_df.Y))) + list(zip(list(h_line_df.X),list(h_line_df.Y)))
            else:  
                line_df = ZD_boundary[q_line_index:z_line_index+1]
                xy_list = list(zip(list(line_df.X),list(line_df.Y)))
            jzx.loc[index] = [*[v for v in value.values],LineString(xy_list)]
        jzx.to_file(savepath,encoding='gb18030',crs=self.ZD.crs)
    
    def ZJDH_format(self):
        """
        格式化JZX数据中的界址号。

        返回:
        - jzxcopy: DataFrame, 格式化后的JZX数据。

        该函数会遍历JZX数据中的每一行，并根据界址号的长度进行不同的格式化处理。
        如果界址号为空，则将其设置为空字符串；如果只有一个界址号，则直接使用该界址号；
        如果有两个界址号，则使用“、”连接两个界址号；如果有两个以上的界址号，则只保留第一个和最后一个界址号。
        """
        jzxcopy = self.JZX.copy()
        for index,row in jzxcopy.iterrows():
            if len(row.ZJDH) == 0:
                jzxcopy.loc[index,'ZJDH'] = ''
            elif len(row.ZJDH) == 1:
                jzxcopy.loc[index,'ZJDH'] = row.ZJDH[0]
            elif len(row.ZJDH) == 2:
                jzxcopy.loc[index,'ZJDH'] = '、'.join(set(row.ZJDH))
            else:
                jzxcopy.loc[index,'ZJDH'] = f"{row.ZJDH[0]}...{row.ZJDH[-1]}"
        return jzxcopy.fillna('')
    
    def hzdh_repeat(self,save):
        """
        检查界址点重复，并将结果保存到Excel文件中。

        参数:
        - save: str, 输出文件的路径。

        该函数会首先复制界址点数据，并添加一个包含界址点代码和界址号的列。
        然后，该函数会统计每个界址点代码和界址号组合的出现次数，并将出现次数大于1的记录保存到Excel文件中。
        """
        jzd_data = self.JZD.copy()
        jzd_data['ZDDM_JZDH'] = jzd_data.ZDDM + jzd_data.JZD_NEW
        countdf = groupby(jzd_data,['ZDDM_JZDH'],'count')
        countdf['ZDDM'] = countdf['ZDDM_JZDH'].str[:19]
        countdf['JZDH'] = countdf['ZDDM_JZDH'].str[19:]
        countdf = countdf[countdf['COUNT']>1]
        countdf.to_excel(save,index=False)
        
                
if __name__ == '__main__':
    Ow = Ownership(r'E:\工作文档\SLLJDJZD2.gdb')
    Ow.set_zddm('三教镇郝家坝村邓家岩村民小组')
    Ow.add_jzx_all()
    Ow.ZJDH_format()
    Ow.JZX.to_excel('JZX34324.xlsx')
    

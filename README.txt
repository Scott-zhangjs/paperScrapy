----------------------------Created in 4.29 2017-------------------------------
1. 本项目主要任务是爬去相关论文的信息

2. mysqlpool.py 自定义了一个mysql的连接池函数，便于使用

3. spiders/dblpSpider.py 对ccf或者给定一个venue名称，找到dblp数据库中对应的dblp名称

4. 当前任务，加入代理

----------------------------Updated  in 5.1 2017-------------------------------
1. 代理设置完毕，速度堪忧

2. 发现新的问题，
	（1）dblp 搜索 Information Processing Letters，volume解析出现问题
	（2）Decision Support Systems，exact matches 多个链接
	（3）Foundations of Computational Mathematics，第一个volume为空
	（4）Journal of Theoretical and Applied Information Technology，Journal of Computer Information Systems，Library and Information Research，Library and Information Science Research，Libres: Library and Information Science Research Electronic Journal

3. 手动更新了3004 Foundations of Computational Mathematics

最新数据整理：

1. CCF表中共有572个venue（包含一个NOT IN CCF），其中28个venue为"NOT IN DBLP"， 4.9%的venue不在dblp中，
   有30个venue存在第二个dblp名（但是有些和第一个是一样的）， 有8个venue存在第三个dblp名。
3. CORE表中共有2566个venue（包含一个NOT IN CORE），其中370个venue为"NOT IN DBLP"，14%的venue不在dblp中，
   有45个venue存在第二个dblp名（但是有些和第一个是一样的）， 有12个venue存在第三个dblp名。
4. CCF表中：
	A: 68个，1个NOT IN DBLP
	B: 230个，8个NOT IN DBLP
	C: 273个，18个NOT IN DBLP
5. CORE表中：
	A*: 124个，12个NOT IN DBLP
	A : 387个， 45个NOT IN DBLP
	B : 679个， 99个NOT IN DBLP
	C : 1258个， 208个NOT IN DBLP
	Australasian: 78个（均为会议）
	其他：39个


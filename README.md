# 用来爬取国内主流直播平台数据 
+ 主要参数 
+ 在线人数
+ 订阅
+ 直播游戏分类
+ 主播名
+ 直播间名
+ 直播间号
> 使用python 3
使用 'scrapy runspider xxxx.py'
使用 docker 来建立mysql

mysql 表

--
-- 表的结构 `bilibili`
--

CREATE TABLE `bilibili` (
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `platform` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `title` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `online` int(11) NOT NULL,
  `fans` int(11) NOT NULL,
  `cate` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `rid` varchar(50) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
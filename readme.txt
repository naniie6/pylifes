version 0.1

this program have used some resources fetched through network: the images, tilemap.py. thank you, the authors !

requires:
  pygame: http://www.pygame.org/download.shtml
  StacklessPython: http://www.stackless.com/

You can execute TestAnimal.py to watch the demo.
If you don't like the gui interface , you can execute "TextAnimal.py -q" to run it quietly, then you can have a look at the interesting logs.
You can write your own animals.

the APIs provided for writing animals :

 * begin_moving( (int, int) ), stop_moving, reset_target( (int, int) )
 * scan() => list of AnimalStats , scanfor( AnimalStat ) => AnimalStat or None

enjoy yourself!

chinese doc:

使用到以下第三方库和工具：
  pygame，请从http://www.pygame.org/download.shtml下载最新版本。 
  StacklessPython，请从http://www.stackless.com/下载相应版本, 直接将stacklesspython提供的python24.dll放到python安装目录下，如果想恢复标准python，将stacklesspython的python24.dll删除或改名即可, 除了直接操作frame的c代码以外，stackless与CPython完全兼容，所以请放心使用。

执行 TestAnimal.py 观看demo。
修改 TestAnimal.py 编写自己的Animal。

执行 setup.py py2exe 或者执行 ToExe.lnk 快截方式可以创建可执行文件。

 * 提供API：begin_moving 、stop_moving，用户可以编写动物以自定义的策略进行移动。
 * 提供API：scan 、scanfor，用户编写的动物可以观察视野范围内的情况，并执行相应的行为。

实现了滚动地图!

enjoy yourself!

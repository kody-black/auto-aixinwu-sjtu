## 新版签到脚本的故事

本来不打算更新了，但是SadPull同学发issue：已经白嫖很久了，突然失效了感觉不习惯呜呜呜

我心真善，更新好了

所以白嫖的同学点个虽然没啥用的star吧，不要默默白嫖了~

## SJTU爱心屋自动签到脚本

有这么一个故事，室友大概半年前写了一个爱心屋签到脚本，我拿来白嫖，但是当时觉得自己币多，而且没听太明白怎么配置，就没有用。

然后半年过去了，室友用白嫖了半年的爱心币过上了幸福的新生活，而我一无所获，只留下无尽的悔恨

但是作为小丑🃏，发现已经找不到室友当年的脚本了（~~为什么不找室友再要一次呢？感觉很丢人是不是~~,GitHub上面的也比较旧用不了，只好自己花了一个晚上重写了一个 🐕

部分参考了[AutoLogin/sjtu-aixinwu/aixinwu pyrtsun/AutoLogin](https://github.com/rtsun/AutoLogin/blob/master/sjtu-aixinwu/aixinwu.py)

欢迎大家白嫖~

## 使用方法

```
git clone https://github.com/distiny-cool/auto-aixinwu-sjtu.git
cd auto-aixinwu-sjtu
pip install -r requirements.txt
cp config_template.py config.py
# 修改config.py为你的用户名和密码
python aixinwu.py
```

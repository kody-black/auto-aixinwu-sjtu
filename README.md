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
# 首次执行需要输入一次用户名和密码，之后会直接用保存的cookie进行登录
python aixinwu.py
```

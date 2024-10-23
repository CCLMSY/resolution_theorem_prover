# Resolution Theorem Prover 一阶逻辑推理器

## 📖 介绍
使用Two-Pointer Resolution算法自动化推理一阶逻辑问题。

开发环境：`Python 3.12.7 on Conda, Windows 11`

如果这个项目对你有帮助，请给个 Star⭐️ 谢谢喵~

## 🎉 使用方法
1. 确保你已安装python环境，将项目解压到同一目录下。
2. 在`input`文件夹下放入符合输入要求的文件，文件名以`1.in`为例。
3. 在当前目录打开终端，输入以下命令，推导过程及结果会在终端展示：
```shell
python.exe .\resolution_theorem_prover.py .\input\1.in
```
4. 如果希望将推导过程及结果保存到文件中，可以使用以下命令：
```shell
python.exe .\resolution_theorem_prover.py .\input\1.in > .\output\1.out
```
5. 推导过程及结果会保存在`output`文件夹下，文件名以`1.out`为例。

## 💬 输入格式
- 请将输入文件放在`input`文件夹下。
- 手动将所有句子转化为合取范式（CNF），再分为若干子句。
  - 本项目采用“反证法”进行推理，结论需要转化为否定形式。
- 输入文件格式：
  - 一行一个子句，子句的函数间以空格分隔。
    - 子句示例：`!func(x,CC) funcb(y)`
    - 形式：[非号]函数名(参数列表)
  - 参数列表中，单个字母视为变量，多个字符视为常量。
  - 参数之间以逗号分隔，单个函数表达式内不含空格。
- 输入文件的格式可参考`input`文件夹下的示例文件。

## 📝 输出格式
- [Read&Mark]：读入子句、标记
- [Clauses]：处理后的子句
- [Process]：具体的推导过程
- [Result]：推导结果

## 📚 示例
### 题目描述
1. All hounds howl at night
2. Anyone who has any cats will not have any mice
3. Light sleepers do not have anything which howls at night
4. John has either a cat or a hound
5. **Prove**: If John is a light sleeper, then John does not have any mice

### 输入文件`1.in`：
```
HowlsAtNight(Hound)
!Has(x,Cat) !Has(x,Mouse)
!LightSleeper(x) !Has(x,y) !HowlsAtNight(y)
Has(John,Cat) Has(John,Hound)
LightSleeper(John)
Has(John,Mouse)
```
### 输出文件`1.out`：
```
[Read&Mark]
Proc 0: HowlsAtNight(Hound)
	const: Hound -> 1
Proc 1: !Has(x,Cat) !Has(x,Mouse)
	var: x -> -1
	const: Cat -> 2
	const: Mouse -> 3
Proc 2: !LightSleeper(x) !Has(x,y) !HowlsAtNight(y)
	var: x -> -2
	var: y -> -3
Proc 3: Has(John,Cat) Has(John,Hound)
	const: John -> 4
Proc 4: LightSleeper(John)
Proc 5: Has(John,Mouse)

[Clauses]
0: HowlsAtNight(1)
1: !Has(-1,2) !Has(-1,3)
2: !LightSleeper(-2) !Has(-2,-3) !HowlsAtNight(-3)
3: Has(4,2) Has(4,1)
4: LightSleeper(4)
5: Has(4,3)

[Process]
Failed Merge: 1 into [0]
Substitution: -3 -> 1
Merge: 	[0, 2] => !LightSleeper(-2) !Has(-2,1)
Failed Merge: 1 into [0, 2]
Substitution: -2 -> 4
Merge: 	[0, 2, 3] => !LightSleeper(4) Has(4,2)
Substitution: -1 -> 4
Merge: 	[0, 1, 2, 3] => !LightSleeper(4) !Has(4,3)
Merge: 	[0, 1, 2, 3, 4] => !Has(4,3)
Merge: 	[0, 1, 2, 3, 4, 5] => 

[Result] Accepted
Substitution Count: 3
Unification Count: 7
```
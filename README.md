# Chinese Legal Text Redactor

一个轻量、离线运行的中文法律文本隐私信息脱敏工具。它可以在本地识别并替换常见的身份证号、手机号码、固定电话、电子邮箱和银行卡号，适合在分享案例、调试文书处理程序或制作演示数据前进行初步清理。

> 项目仍处于早期阶段。正则规则无法覆盖所有写法，也可能产生误判；正式公开法律文书前，必须由专业人员再次人工检查。

## 特点

- 完全离线，不上传文本
- 仅使用 Python 标准库，无运行时依赖
- 支持文件、标准输入和 Python API
- 可指定只处理部分敏感信息类型
- 输出各类型替换数量，便于复核

## 快速开始

要求 Python 3.10 或更高版本。

```bash
python -m pip install -e .
cn-legal-redactor example.txt -o example.redacted.txt
```

也可以使用管道：

```bash
echo "联系电话：13800138000" | cn-legal-redactor
```

输出：

```text
联系电话：[MOBILE]
```

只处理身份证号和邮箱：

```bash
cn-legal-redactor example.txt --types id_card,email
```

## Python API

```python
from cn_legal_redactor import redact_text, redact_with_report

cleaned = redact_text("邮箱：someone@example.com")
result = redact_with_report("电话：13800138000")

print(cleaned)
print(result.text, result.counts)
```

## 支持的类型

| 类型 | 占位符 | 说明 |
| --- | --- | --- |
| `id_card` | `[ID_CARD]` | 15位或18位中国居民身份证号 |
| `mobile` | `[MOBILE]` | 中国大陆手机号码，可含 `+86` |
| `phone` | `[PHONE]` | 带区号的固定电话号码 |
| `email` | `[EMAIL]` | 常见电子邮箱地址 |
| `bank_card` | `[BANK_CARD]` | 16至19位银行卡号，可含空格或短横线 |

## 开发与测试

```bash
python -m unittest discover -s tests -v
```

欢迎提交问题和改进建议。参与贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 隐私与责任说明

本工具只提供初步、自动化的文本清理能力，不构成法律意见，也不能替代发布前的人工审核。使用者应根据适用法律、司法公开规则和所在机构的保密要求处理文书及个人信息。

## 许可证

[MIT License](LICENSE)

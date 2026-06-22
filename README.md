# Agent Company

一个可以直接在 Codex 终端里运行的“多 agent 公司”MVP。

你给公司一个目标，`总经理`会负责拆任务、安排岗位 agent、汇总交付物、检查风险并给出下一步。

## 运行

```bash
python3 -m agent_company "帮我做一个 AI 自动化咨询公司"
```

带限制条件：

```bash
python3 -m agent_company "帮我做一个 AI 自动化咨询公司" \
  --constraint "不使用浏览器" \
  --constraint "第一版必须一周内能跑"
```

导出 JSON 报告：

```bash
python3 -m agent_company --json --save reports/first-run.json "帮我做一个 AI 自动化咨询公司"
```

## 当前公司结构

- `总经理`：拆解目标、安排任务、检查覆盖、输出复盘和下一步。
- `市场研究员`：用户、竞品、机会窗口。
- `产品经理`：MVP、流程、验收标准。
- `工程师`：技术路径、数据模型、测试方案。
- `设计师`：交互原则、信息层级、终端输出体验。
- `增长运营`：渠道、话术、指标、实验计划。
- `财务法务`：预算、权限、审批、合规边界。

## 测试

```bash
python3 -m unittest discover -s tests
```

## 下一步可以升级什么

- 把当前确定性 agent 替换为真实 LLM 执行器。
- 增加长期记忆，让每次公司会议的结果进入知识库。
- 加审批系统：付款、发邮件、改线上代码、签合同前必须让老板确认。
- 加真实工具：文件、Git、邮件、日历、飞书/Slack、Notion、数据库。

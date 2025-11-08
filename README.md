## What traits shape a good career start: Industry, Occupation and Education Analysis for Young Singaporeans aged 25 to 29. 是什么特征塑造了良好的职业起点：——针对新加坡 25 至 29 岁青年群体的行业、职业与教育分析

---

## 💡 Project Overview / 项目概览

This interactive Streamlit dashboard analyzes Singapore’s employment, salary, education, and unemployment trends (2007–2024) to help young residents (aged 25–29) discover which industries and occupations offer the best career prospects.
It draws data from Singapore’s official Ministry of Manpower (MOM) statistics and visualizes long-term trends in **youth employment shares, salary growth, and education levels**.

本项目通过 Streamlit 构建的交互式仪表板，分析了新加坡 **2007–2024** 年的就业、薪资、教育与失业趋势，旨在帮助25–29 岁青年发掘最具潜力的行业与职业方向。
数据来源于新加坡人力部官方公开数据，重点展示 **青年就业占比、薪资走势及教育结构变化**，为求职与政策研究提供参考。

---

## 🧩 Features / 主要功能

* 📊 **Overall Employment Trends** — visualize total resident employment and year-on-year growth.
* 👩‍💼 **Youth Share by Industry (2024)** — discover which industries attract more young workers and ompare manufacturing, construction, and service sector performance.
* 💰 **Median Salary by Occupation & Gender** — explore wage differences across roles and time.
* 🎓 **Education Attainment Trends (25–29)** — track the “educational upgrade” toward university degrees.
* 📈 **Unemployment by Education Level** — evaluate resilience during economic downturns (1992–2024).
* 🧮 **Downloadable CSV & Treemap/Bar/Line Visualizations** for further research and analysis.  


* 📊 **总体就业趋势** — 查看居民就业总量与年度增长率。
* 👩‍💼 **行业青年占比（2024）** — 探索哪些行业更吸引年轻人，并对比制造业、建筑业与服务业的表现。
* 💰 **职业与性别薪资中位数趋势** — 观察不同岗位与性别的长期薪资变化。
* 🎓 **25–29 岁学历结构趋势** — 揭示“教育升级”现象，大学学历成新常态。
* 📈 **按学历划分的失业率趋势** — 分析经济波动期各学历群体的韧性。
* 🧮 **数据导出与可视化下载功能** — 方便研究与教学使用。

---

## 🔍 Key Findings / 核心发现

### Industry Perspective / 行业视角

* From **2007 to 2024**, Singapore’s total employment steadily increased, though growth slowed after COVID-19 due to global economic headwinds.
* **Services sector** dominates the landscape for young workers, especially in **Professional, Financial, and Public Administration & Education** services.
* **Youth share** is declining in traditional industries (Manufacturing, Construction) and shifting toward **knowledge-intensive sectors** like Information & Communications.

* **2007–2024 年**，新加坡就业总量总体稳步上升，但疫情后增长放缓，转向结构优化。
* **服务业** 长期占据主导地位，年轻人主要集中于 **专业服务、金融保险、公共行政与教育** 等领域。
* 青年就业比例正在从传统行业（制造、建筑）转向 **知识密集型行业（信息通信等）**。

### Occupation Perspective / 职业视角

* The 25–29 age group is dominated by **Professionals (≈39%)** and **Associate Professionals & Technicians (≈32%)**, together forming almost **three-quarters** of all employed youth.
* Traditional blue-collar jobs (craftsmen, machine operators, cleaners) have fallen below **5%**, indicating automation and service-sector expansion.
* The median salary gap between occupations remains large — **managers and professionals** earn 2–3× more than service or manual workers.
* Gender differences exist but are **smaller than occupational differences**; occupation is the true driver of wage disparity.


* 年龄 25–29 岁人群主要集中在 **专业人员（约39%）** 与 **助理专业/技术人员（约32%）**，合计近 **75% 的青年就业者**。
* 蓝领岗位（技工、操作员、清洁工）占比已降至 **5% 以下**，反映自动化与服务业扩张。
* 不同职业间薪资差距显著，**管理与专业职位** 的中位数收入是体力或服务岗位的 2–3 倍。
* 性别薪酬差距存在但较小，**职业类型** 才是决定工资差异的关键。

### Education Perspective / 教育视角

* A clear **“educational upgrade”** is visible — university graduates now make up nearly **60%** of the 25–29 cohort.
* **Secondary and below** education levels have sharply declined since 2007.
* Those with **post-secondary diplomas** face the highest unemployment risk since 2009 — the “**squeezed middle**” effect:
  caught between degree-holders (competition) and lower-skilled jobs (overqualification).
* During crises (2008, 2020), low-educated groups’ unemployment rates surged most, while degree-holders remained more stable — education acts as a **“life jacket”** in recessions.

  
* 出现明显的 **“学历升级”趋势** —— 大学学历已占 25–29 岁人群的约 **60%**。
* **中学及以下学历** 比例自 2007 年后大幅下降。
* **大专/文凭层次** 就业风险最高，出现“**中间层被挤压**”现象：既被高学历竞争，又被低技能岗位排斥。
* 在经济危机（2008、2020）中，低学历群体失业率上升最剧烈；而大学学历者波动最小，学历犹如“**经济救生衣**”。

---

## ⚙️ Code Execution Guide / 代码运行指南

**Run the Streamlit:**
open the new terminal

```bash
streamlit Dashboard.py
```

---

## 📚 Data Source / 数据来源
* [Singapore Ministry of Manpower (MOM) — *Resident Employment, Unemployment & Wages Statistics (2007–2024)*](https://www.tablebuilder.singstat.gov.sg/)

